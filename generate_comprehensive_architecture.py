import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rounded_card(ax, x, y, width, height, title, subtitle, items, bg_color, border_color, title_color='#0f172a', badge=None):
    # Main card box
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.6,rounding_size=1.2",
        fc=bg_color, ec=border_color, lw=1.8, zorder=2
    )
    ax.add_patch(box)
    
    # Title bar
    ax.text(x + 1.2, y + height - 2.8, title, fontsize=10, fontweight='bold', color=title_color, zorder=3, va='top')
    
    if badge:
        b_box = patches.FancyBboxPatch(
            (x + width - 13.5, y + height - 3.8), 12.5, 2.6,
            boxstyle="round,pad=0.2,rounding_size=0.6",
            fc=border_color, ec='none', zorder=3
        )
        ax.add_patch(b_box)
        ax.text(x + width - 7.25, y + height - 2.5, badge, fontsize=7.5, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)

    if subtitle:
        ax.text(x + 1.2, y + height - 5.2, subtitle, fontsize=8, fontstyle='italic', color='#475569', zorder=3, va='top')
        start_item_y = y + height - 8.0
    else:
        start_item_y = y + height - 6.0
        
    line_spacing = (start_item_y - y - 1.0) / max(len(items), 1)
    for i, item in enumerate(items):
        item_y = start_item_y - (i * min(line_spacing, 3.2))
        ax.text(x + 1.5, item_y, f"• {item}", fontsize=7.8, color='#1e293b', zorder=3, va='top')

def generate_comprehensive_architecture():
    fig, ax = plt.subplots(figsize=(18, 10.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#f8fafc')

    # Header / Title Block
    ax.text(50, 97.8, "FEDERATED MULTI-AGENT QWEN + JEV DECISION INTELLIGENCE", ha='center', va='center', fontsize=18, fontweight='heavy', color='#0f172a', fontfamily='sans-serif')
    ax.text(50, 95.0, "End-to-End Enterprise Architecture: Decentralized LoRA Training, FedAvg Parameter Merge, System 1 Calibrated JEV-9B Inference & Synthesis", ha='center', va='center', fontsize=9.5, color='#475569')

    # Tier Dividers / Zones
    # Zone 1: Offline Federated Training (Left, x: 2 to 32)
    zone1 = patches.FancyBboxPatch((1.5, 2.0), 31.0, 90.5, boxstyle="round,pad=1.0,rounding_size=1.5", fc='#ffffff', ec='#cbd5e1', lw=1.2, ls='--')
    ax.add_patch(zone1)
    ax.text(17.0, 90.2, "TIER 1: OFFLINE FEDERATED TRAINING", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#047857')
    ax.text(17.0, 88.2, "(Decentralized Privacy & FedAvg Aggregation)", ha='center', va='center', fontsize=8, color='#64748b')

    # Zone 2: Model Management & Runtime Execution (Middle-Left, x: 34 to 64)
    zone2 = patches.FancyBboxPatch((34.0, 2.0), 31.0, 90.5, boxstyle="round,pad=1.0,rounding_size=1.5", fc='#ffffff', ec='#cbd5e1', lw=1.2, ls='--')
    ax.add_patch(zone2)
    ax.text(49.5, 90.2, "TIER 2: RUNTIME INFERENCE & JEV-9B", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#1d4ed8')
    ax.text(49.5, 88.2, "(VRAM Swapper & System 1 Linear Head Projection)", ha='center', va='center', fontsize=8, color='#64748b')

    # Zone 3: Synthesis, Comparison & UI Cockpit (Right, x: 66.5 to 98.5)
    zone3 = patches.FancyBboxPatch((66.5, 2.0), 32.0, 90.5, boxstyle="round,pad=1.0,rounding_size=1.5", fc='#ffffff', ec='#cbd5e1', lw=1.2, ls='--')
    ax.add_patch(zone3)
    ax.text(82.5, 90.2, "TIER 3: SYNTHESIS, API & BANKING UX", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#7e22ce')
    ax.text(82.5, 88.2, "(Conflict Resolution, SAR Dossier & Cockpit)", ha='center', va='center', fontsize=8, color='#64748b')

    # ==========================
    # CARDS IN TIER 1
    # ==========================
    # 1. Dataset Partition
    draw_rounded_card(
        ax, x=3.5, y=72.0, width=27.0, height=14.0,
        title="FinGPT Private Dataset",
        subtitle="FinGPT/fingpt-fiqa_qa (17,110 examples)",
        items=[
            "Agent 1 Partition: 8,555 QA Fraud pairs",
            "Agent 2 Partition: 8,555 QA AML & Risk pairs",
            "Decentralized: Raw data never leaves node",
            "Preserves strict institutional data privacy"
        ],
        bg_color='#f0fdf4', border_color='#16a34a', title_color='#15803d', badge="Data Tier"
    )

    # 2. Agent 1 Local LoRA Training
    draw_rounded_card(
        ax, x=3.5, y=52.0, width=27.0, height=17.5,
        title="Agent 1: Fraud Node (PEFT)",
        subtitle="Base: Qwen2.5-0.5B-Instruct | LoRA (r=8, α=16)",
        items=[
            "Domain: Velocity & Payment Egress Anomaly",
            "Target: q_proj, v_proj, k_proj, o_proj",
            "Output: adapter_model.safetensors (24MB)",
            "Path: qwen/agent1/adapter_config.json",
            "Zero client data transmission to central server"
        ],
        bg_color='#ecfdf5', border_color='#10b981', title_color='#065f46', badge="Client 1"
    )

    # 3. Agent 2 Local LoRA Training
    draw_rounded_card(
        ax, x=3.5, y=29.0, width=27.0, height=17.5,
        title="Agent 2: Risk & AML Node (PEFT)",
        subtitle="Base: Qwen2.5-0.5B-Instruct | LoRA (r=8, α=16)",
        items=[
            "Domain: AML, Structuring & BSA Compliance",
            "Specialization: 31 U.S.C. § 5324, SAR criteria",
            "Output: adapter_model.safetensors (24MB)",
            "Path: qwen/agent2/adapter_config.json",
            "Adversarial challenger role in deliberation"
        ],
        bg_color='#fdf4ff', border_color='#c026d3', title_color='#86198f', badge="Client 2"
    )

    # 4. FedAvg Aggregator
    draw_rounded_card(
        ax, x=3.5, y=5.0, width=27.0, height=21.0,
        title="FedAvg Parameter Aggregator",
        subtitle="Federated Averaging Protocol: w* = 0.5*w1 + 0.5*w2",
        items=[
            "Aggregates adapter tensor weights offline",
            "Generates synchronized global consensus LoRA",
            "Saves artifact to: qwen/global_qwen/",
            "Guarantees privacy-preserving knowledge transfer",
            "Synchronized initialization across local epochs",
            "Shared foundation for global consensus validation"
        ],
        bg_color='#eff6ff', border_color='#3b82f6', title_color='#1e40af', badge="FedAvg"
    )

    # ==========================
    # CARDS IN TIER 2
    # ==========================
    # 5. Model Manager & Memory Optimizer
    draw_rounded_card(
        ax, x=36.0, y=70.0, width=27.0, height=16.0,
        title="ModelManager & VRAM Swapper",
        subtitle="Memory-Safe Runtime on NVIDIA RTX 2050 (4GB)",
        items=[
            "Single frozen base Qwen2.5-0.5B loaded (~0.9GB)",
            "Dynamic LoRA adapter swapping via PEFT API",
            "Hot-swap: agent1 ↔ agent2 ↔ global_qwen",
            "Zero GPU reload penalty (<10ms swap latency)",
            "CUDA 12.1 accelerated bfloat16/float16 execution"
        ],
        bg_color='#f8fafc', border_color='#0284c7', title_color='#0369a1', badge="VRAM Safe"
    )

    # 6. Concurrent Multi-Agent Inference
    draw_rounded_card(
        ax, x=36.0, y=41.0, width=27.0, height=26.0,
        title="Concurrent Inference Pipeline",
        subtitle="inference/pipeline.py with Parallel Orchestration",
        items=[
            "User Transaction & Context ingested",
            "Async Execution: Agent 1 & Agent 2 dispatched",
            "Agent 1 generates natural language fraud analysis",
            "Agent 2 produces critical counter-arguments",
            "Global Qwen runs synchronized consensus evaluation",
            "Key factors & uncertainty markers parsed dynamically",
            "Live streaming stage callbacks to WebSockets",
            "Sub-second response timing on local hardware"
        ],
        bg_color='#eef2ff', border_color='#6366f1', title_color='#3730a3', badge="Pipeline"
    )

    # 7. JEV-9B Decision Intelligence System 1
    draw_rounded_card(
        ax, x=36.0, y=5.0, width=27.0, height=33.0,
        title="autotrust/JEV-9B Decision Head",
        subtitle="System 1 Linear Projection & Mathematical Calibration",
        items=[
            "Genuine Safetensors: jev/head.safetensors",
            "Weight Matrix W: [24, 4096] | Bias b: [24]",
            "Temperature Calibration: jev/calibration.json",
            "Calibrated Temperature T_noul = 1.002217823669",
            "24 Decision Verbalizer Slots (Slot 0=False, Slot 1=True)",
            "Rigorous Anti-Fabrication Directive:",
            "  • No mock random confidence generators",
            "  • Real mathematical probability normalization",
            "  • Transparent local audit mode on RTX 2050 GPU"
        ],
        bg_color='#faf5ff', border_color='#9333ea', title_color='#6b21a8', badge="JEV-9B"
    )

    # ==========================
    # CARDS IN TIER 3
    # ==========================
    # 8. Comparison & Synthesis Engine
    draw_rounded_card(
        ax, x=69.0, y=65.0, width=27.0, height=21.0,
        title="Comparison & Synthesis Layer",
        subtitle="services/comparison.py Institutional Gate",
        items=[
            "Evaluates Agreement vs Stance Disparity",
            "Classifies state into 3 Discrete Operational Modes:",
            "  • CONSENSUS: Stances align & Conf >= 0.55",
            "  • DISAGREEMENT: Opposing risk conclusions",
            "  • UNCERTAIN: High ambiguity / low confidence",
            "Synthesizes supporting & contradictory factor ledger",
            "Flags missing KYC, clearing rails, or CTR evidence",
            "Aligns final verdict with global federated model"
        ],
        bg_color='#fff7ed', border_color='#ea580c', title_color='#c2410c', badge="Synthesizer"
    )

    # 9. FastAPI Orchestration Layer
    draw_rounded_card(
        ax, x=69.0, y=39.0, width=27.0, height=23.0,
        title="FastAPI Orchestration API",
        subtitle="backend/main.py (Port 8000, Host 0.0.0.0)",
        items=[
            "POST /api/chat: Full multi-agent synthesis payload",
            "GET /api/model-info: Model metadata & audit trail",
            "GET /api/jev/artifacts: Tensor inspection & slots",
            "GET /health: Online liveness & CUDA GPU status",
            "WebSocket /ws/inference: Real-time token streaming",
            "Pydantic V2 Schemas for bulletproof validation",
            "CORS enabled for enterprise front-end integration"
        ],
        bg_color='#eff6ff', border_color='#2563eb', title_color='#1e40af', badge="FastAPI"
    )

    # 10. React + Vite Interactive Banking Cockpit
    draw_rounded_card(
        ax, x=69.0, y=5.0, width=27.0, height=31.0,
        title="React 19 Enterprise Banking UI",
        subtitle="frontend/ (Port 5173, Vite Dev Server)",
        items=[
            "Institutional Banking Dark/Light Theme",
            "Dynamic SVG Risk Score Donut (P(True) 97.8%)",
            "Dual-Agent Comparison Matrix with Stance Badges",
            "Forensic Key Factors Breakdown (Supporting/Challenging)",
            "Automated SAR Dossier Generator (FinCEN Format):",
            "  • MT103 Wire Data & Structuring Pattern",
            "  • 31 U.S.C. § 5324 & 18 U.S.C. § 1956 cites",
            "  • Hard Hold & IRREVOCABLE SWIFT Directives",
            "Real-time WebSocket Live Deliberation Tracker"
        ],
        bg_color='#f0fdf4', border_color='#15803d', title_color='#166534', badge="React 19"
    )

    # ==========================
    # CONNECTING ARROWS & DATA FLOWS
    # ==========================
    def connect_arrow(x1, y1, x2, y2, color='#64748b', lw=1.6, label=None, label_pos=(0, 0), rad=0.0):
        con = patches.ConnectionPatch(
            xyA=(x2, y2), xyB=(x1, y1),
            coordsA="data", coordsB="data",
            arrowstyle="->,head_width=0.4,head_length=0.6",
            lw=lw, color=color,
            connectionstyle=f"arc3,rad={rad}", zorder=5
        )
        ax.add_artist(con)
        if label:
            ax.text(label_pos[0], label_pos[1], label, fontsize=7.5, fontweight='bold', color=color, zorder=6, ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", fc='#ffffff', ec=color, lw=1))

    # Flow 1: Dataset to Agent 1 & Agent 2
    connect_arrow(17.0, 72.0, 17.0, 69.5, color='#10b981', label="Partition D1", label_pos=(17.0, 70.8))
    connect_arrow(17.0, 52.0, 17.0, 46.5, color='#c026d3', label="Partition D2", label_pos=(17.0, 49.3))

    # Flow 2: Agent 1 & Agent 2 to FedAvg
    connect_arrow(17.0, 29.0, 17.0, 26.0, color='#3b82f6', label="LoRA Weights (W1, W2)", label_pos=(17.0, 27.5))

    # Flow 3: Tier 1 FedAvg to Tier 2 ModelManager & Pipeline
    connect_arrow(30.5, 15.0, 36.0, 78.0, color='#0284c7', rad=-0.25, label="Global Adapter", label_pos=(33.2, 55.0))
    connect_arrow(30.5, 60.0, 36.0, 55.0, color='#10b981', rad=-0.1, label="W1 LoRA", label_pos=(33.2, 63.0))
    connect_arrow(30.5, 37.0, 36.0, 48.0, color='#c026d3', rad=0.1, label="W2 LoRA", label_pos=(33.2, 42.0))

    # Flow 4: ModelManager to Pipeline
    connect_arrow(49.5, 70.0, 49.5, 67.0, color='#0284c7', label="Adapter Hot-Swap", label_pos=(49.5, 68.5))

    # Flow 5: Pipeline to JEV Head
    connect_arrow(49.5, 41.0, 49.5, 38.0, color='#9333ea', label="Reasoning & Representations", label_pos=(49.5, 39.5))

    # Flow 6: Pipeline & JEV to Synthesis Layer
    connect_arrow(63.0, 54.0, 69.0, 75.0, color='#ea580c', rad=-0.15, label="Raw Agent Stances", label_pos=(66.0, 68.0))
    connect_arrow(63.0, 22.0, 69.0, 70.0, color='#9333ea', rad=-0.25, label="Calibrated P(True)", label_pos=(66.0, 40.0))

    # Flow 7: Synthesis to FastAPI
    connect_arrow(82.5, 65.0, 82.5, 62.0, color='#2563eb', label="Final Decision Payload", label_pos=(82.5, 63.5))

    # Flow 8: FastAPI to React UI
    connect_arrow(82.5, 39.0, 82.5, 36.0, color='#15803d', label="REST / WebSocket", label_pos=(82.5, 37.5))

    plt.tight_layout()
    output_path = 'architecture_flow_v2.png'
    plt.savefig(output_path, bbox_inches='tight')
    plt.savefig('architecture_diagram.png', bbox_inches='tight')
    plt.close()
    print(f"Created {output_path} and updated architecture_diagram.png successfully!")

if __name__ == '__main__':
    generate_comprehensive_architecture()
