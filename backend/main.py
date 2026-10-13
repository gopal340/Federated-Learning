"""
FastAPI Server for Federated Qwen + JEV Decision Intelligence System.

Provides:
  - POST /api/chat : Concurrent execution of Agent 1 and Agent 2 + Comparison + Final Decision
  - GET /api/model-info : Operational and architectural metadata of the real package
  - GET /api/jev/artifacts : Detailed technical inspection of JEV decision-head artifacts
  - WebSocket /ws/inference : Live streaming of agent stages and token progression
"""
import os
import time
import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

from schemas.responses import (
    ChatRequest, ChatResponse, AgentResult, ComparisonResult,
    FinalResult, SharedModelResult, ModelInfo, InferenceStatus
)
from model_manager import ModelManager
from agents.agent1 import AGENT1_SYSTEM_PROMPT, AGENT1_ADAPTER, AGENT1_ID, AGENT1_ROLE
from agents.agent2 import AGENT2_SYSTEM_PROMPT, AGENT2_ADAPTER, AGENT2_ID, AGENT2_ROLE
from inference.pipeline import (
    run_agent_pipeline, run_shared_federated_pipeline,
    is_banking_scenario, build_out_of_scope_response
)
from services.comparison import compare_agents, synthesize_final_decision

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("api")

# Configuration paths
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = os.getenv(
    "MODEL_ARTIFACTS_DIR",
    str(BASE_DIR.parent / "FINAL_FEDERATED_QWEN_JEV_V2")
)
DEVICE = os.getenv("DEVICE", "cuda")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "60"))

# Global ModelManager instance
model_manager: ModelManager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: loads all genuine model artifacts at startup."""
    global model_manager
    logger.info("Initializing application models and artifacts...")
    try:
        model_manager = ModelManager(artifacts_dir=ARTIFACTS_DIR, device=DEVICE)
        model_manager.load_all()
        logger.info("✓ ModelManager fully initialized and ready.")
    except Exception as e:
        logger.error(f"Error during startup model loading: {e}", exc_info=True)
    yield
    logger.info("Application shutting down.")


app = FastAPI(
    title="Federated Qwen + JEV Decision Intelligence",
    description="Multi-agent decision system combining Federated Qwen LoRA reasoning with JEV Decision Intelligence.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "models_loaded": model_manager.is_loaded if model_manager else False,
        "device": model_manager.device if model_manager else "unknown",
        "artifacts_dir": ARTIFACTS_DIR,
    }


@app.get("/api/model-info", response_model=Dict[str, Any])
async def get_model_information():
    """Returns actual model metadata, fine-tuning details, and JEV artifacts."""
    if not model_manager or not model_manager.is_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded yet")
    return model_manager.get_model_info()


@app.get("/api/jev/artifacts")
async def get_jev_artifacts():
    """Detailed inspection of the real JEV decision-head artifacts."""
    if not model_manager or not model_manager.is_loaded or not model_manager.jev_engine:
        raise HTTPException(status_code=503, detail="JEV engine not loaded")
    return model_manager.jev_engine.get_artifact_details()


@app.post("/api/chat", response_model=ChatResponse)
async def chat_decision(req: ChatRequest):
    """
    Primary decision endpoint:
      1. Runs Agent 1 (Analytical) & Agent 2 (Critical) concurrently
      2. Executes JEV decision pipeline
      3. Compares findings in the Comparison Layer
      4. Synthesizes Final Consensus / Disagreement / Uncertainty result
    """
    if not model_manager or not model_manager.is_loaded:
        raise HTTPException(status_code=503, detail="Model engine not loaded")

    start_time = time.time()
    logger.info(f"Incoming decision request: '{req.question[:60]}...'")

    # Domain Guardrail: Reject non-banking queries immediately with clear reasoning
    if not is_banking_scenario(req.question):
        logger.info("Non-banking domain detected. Returning out-of-scope rejection response.")
        raw_out = build_out_of_scope_response(req.question)
        return ChatResponse(
            agent1=AgentResult(**raw_out["agent1"]),
            agent2=AgentResult(**raw_out["agent2"]),
            shared_model=SharedModelResult(**raw_out["shared_model"]),
            comparison=ComparisonResult(**raw_out["comparison"]),
            final=FinalResult(**raw_out["final"]),
            total_processing_time_ms=(time.time() - start_time) * 1000.0,
        )

    # Run Agent 1 and Agent 2 concurrently
    agent1_task = run_agent_pipeline(
        model_manager=model_manager,
        adapter_name=AGENT1_ADAPTER,
        agent_id=AGENT1_ID,
        role=AGENT1_ROLE,
        system_prompt=AGENT1_SYSTEM_PROMPT,
        user_question=req.question,
        context=req.context,
        max_new_tokens=MAX_NEW_TOKENS,
    )

    agent2_task = run_agent_pipeline(
        model_manager=model_manager,
        adapter_name=AGENT2_ADAPTER,
        agent_id=AGENT2_ID,
        role=AGENT2_ROLE,
        system_prompt=AGENT2_SYSTEM_PROMPT,
        user_question=req.question,
        context=req.context,
        max_new_tokens=MAX_NEW_TOKENS,
    )

    # Concurrency execution
    agent1_raw, agent2_raw = await asyncio.gather(agent1_task, agent2_task)

    agent1_res = AgentResult(**agent1_raw)
    agent2_res = AgentResult(**agent2_raw)

    # Comparison Layer
    comparison_res = compare_agents(agent1_res, agent2_res)

    # Central Shared Federated Global Model Execution (qwen/global_qwen + JEV Consensus)
    shared_raw = await run_shared_federated_pipeline(
        model_manager=model_manager,
        user_question=req.question,
        agent1_res=agent1_raw,
        agent2_res=agent2_raw,
    )
    shared_model_res = SharedModelResult(**shared_raw)

    # Final Decision Synthesis
    final_res = synthesize_final_decision(agent1_res, agent2_res, comparison_res)
    # Align final consensus with the shared federated model
    if comparison_res.status == "CONSENSUS":
        final_res.confidence = shared_model_res.confidence
        final_res.reason = shared_model_res.reasoning

    total_elapsed = (time.time() - start_time) * 1000.0

    return ChatResponse(
        agent1=agent1_res,
        agent2=agent2_res,
        shared_model=shared_model_res,
        comparison=comparison_res,
        final=final_res,
        total_processing_time_ms=total_elapsed,
    )


@app.websocket("/ws/inference")
async def websocket_inference(websocket: WebSocket):
    """
    WebSocket endpoint for live streaming inference status updates.
    Enables the UI to visibly track both agents processing concurrently.
    """
    await websocket.accept()
    logger.info("WebSocket client connected to /ws/inference")

    async def send_status(agent: str, stage: str, message: str, data: dict = None):
        try:
            await websocket.send_json({
                "agent": agent,
                "stage": stage,
                "message": message,
                "timestamp": time.time(),
                "data": data or {},
            })
        except Exception:
            pass

    try:
        while True:
            data = await websocket.receive_json()
            question = data.get("question", "")
            context = data.get("context", None)

            if not question:
                await websocket.send_json({"error": "Question is required"})
                continue

            await websocket.send_json({"stage": "started", "message": "Inference initialized"})

            if not is_banking_scenario(question):
                raw_out = build_out_of_scope_response(question)
                response = ChatResponse(
                    agent1=AgentResult(**raw_out["agent1"]),
                    agent2=AgentResult(**raw_out["agent2"]),
                    shared_model=SharedModelResult(**raw_out["shared_model"]),
                    comparison=ComparisonResult(**raw_out["comparison"]),
                    final=FinalResult(**raw_out["final"]),
                    total_processing_time_ms=5.0,
                )
                await websocket.send_json({
                    "stage": "complete",
                    "result": response.dict(),
                })
                continue

            # Define callbacks for both agents
            async def a1_cb(agent_id, stage, msg, payload=None):
                await send_status(agent_id, stage, msg, payload)

            async def a2_cb(agent_id, stage, msg, payload=None):
                await send_status(agent_id, stage, msg, payload)

            # Run concurrently
            t_start = time.time()
            a1_future = run_agent_pipeline(
                model_manager=model_manager,
                adapter_name=AGENT1_ADAPTER,
                agent_id=AGENT1_ID,
                role=AGENT1_ROLE,
                system_prompt=AGENT1_SYSTEM_PROMPT,
                user_question=question,
                context=context,
                status_callback=a1_cb,
                max_new_tokens=MAX_NEW_TOKENS,
            )

            a2_future = run_agent_pipeline(
                model_manager=model_manager,
                adapter_name=AGENT2_ADAPTER,
                agent_id=AGENT2_ID,
                role=AGENT2_ROLE,
                system_prompt=AGENT2_SYSTEM_PROMPT,
                user_question=question,
                context=context,
                status_callback=a2_cb,
                max_new_tokens=MAX_NEW_TOKENS,
            )

            a1_raw, a2_raw = await asyncio.gather(a1_future, a2_future)

            agent1_res = AgentResult(**a1_raw)
            agent2_res = AgentResult(**a2_raw)

            await send_status("orchestrator", "comparing", "Evaluating agent outputs in comparison layer...")
            comparison_res = compare_agents(agent1_res, agent2_res)
            final_res = synthesize_final_decision(agent1_res, agent2_res, comparison_res)

            total_ms = (time.time() - t_start) * 1000.0

            response = ChatResponse(
                agent1=agent1_res,
                agent2=agent2_res,
                comparison=comparison_res,
                final=final_res,
                total_processing_time_ms=total_ms,
            )

            try:
                await websocket.send_json({
                    "stage": "complete",
                    "result": response.dict(),
                })
            except Exception:
                pass

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({"stage": "error", "error": str(e)})
        except Exception:
            pass
