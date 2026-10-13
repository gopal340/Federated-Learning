import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_review2_presentation():
    src_path = r'C:\Users\adavi\Downloads\SDP_PROJECT (1).pptx'
    backup_path = r'C:\Users\adavi\Downloads\SDP_PROJECT (1)_backup.pptx'
    out_review2_path = r'C:\Users\adavi\Downloads\SDP_PROJECT_REVIEW_2.pptx'
    
    # 1. Create a backup of the original file if not exists
    if not os.path.exists(backup_path):
        shutil.copyfile(src_path, backup_path)
        print(f"Created backup at {backup_path}")

    prs = Presentation(src_path)
    print(f"Original presentation loaded: {len(prs.slides)} slides")

    # The 12th slide is the original 'Thank you' slide.
    # We will remove it from index 11 so that slides 0 to 10 (Review 1 slides 1 to 11) remain exactly as they were.
    if len(prs.slides) >= 12:
        rId = prs.slides._sldIdLst[11].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[11]
        print(f"Original Thank You slide removed to place after Review 2 slides. Current slides: {len(prs.slides)}")

    logo_path = 'extracted_header_logo.png'
    arch_img_path = 'architecture_diagram.png'
    patterns_img_path = 'design_patterns_ux.png'
    demo_img_path = 'system_demo_diagram.png'

    # Template coordinates (matching existing slides)
    LOGO_LEFT = Emu(9003134)
    LOGO_TOP = Emu(195731)
    LOGO_W = Emu(3087633)
    LOGO_H = Emu(497772)

    LINE_LEFT = Emu(-28199)
    LINE_TOP = Emu(898733)
    LINE_W = Emu(12212800)
    LINE_H = Emu(46800)

    TITLE_LEFT = Emu(218175)
    TITLE_TOP = Emu(200000)
    TITLE_W = Emu(8600000)
    TITLE_H = Emu(680000)

    CONTENT_LEFT = Emu(432619)
    CONTENT_TOP = Emu(1120000)
    CONTENT_W = Emu(11346426)
    CONTENT_H = Emu(5350000)

    def add_base_slide(title_text):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
        
        # Add logo
        slide.shapes.add_picture(logo_path, LOGO_LEFT, LOGO_TOP, LOGO_W, LOGO_H)
        
        # Add dividing line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, LINE_LEFT, LINE_TOP, LINE_W, LINE_H)
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(89, 89, 89)
        line.line.color.rgb = RGBColor(89, 89, 89)

        # Add title
        tx_box = slide.shapes.add_textbox(TITLE_LEFT, TITLE_TOP, TITLE_W, TITLE_H)
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Times New Roman'
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(15, 23, 42)
        return slide

    # -------------------------------------------------------------
    # SLIDE 12: Review 2 Expectations & Deliverables Overview Table
    # -------------------------------------------------------------
    s12 = add_base_slide("Review – 2: Expectations & Deliverables")
    t12_shape = s12.shapes.add_table(7, 4, CONTENT_LEFT, CONTENT_TOP, CONTENT_W, Emu(5100000))
    t12 = t12_shape.table
    t12.columns[0].width = Emu(1000000)  # SL No
    t12.columns[1].width = Emu(4400000)  # Expectations
    t12.columns[2].width = Emu(3946426)  # Deliverables
    t12.columns[3].width = Emu(2000000)  # Status

    headers_12 = ["SL No.", "Review 2 Expectations", "Deliverables", "Status & Slide"]
    for c_idx, h in enumerate(headers_12):
        cell = t12.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Times New Roman'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3] else PP_ALIGN.LEFT

    rows_12 = [
        ("1.", "Prepare system requirements based on the review of literature.", "Functional and Non-functional requirements", "Completed\n(Slides 13–14)"),
        ("2.", "Design a suitable architectural framework/system model.", "Architectural framework diagram & tier model", "Completed\n(Slide 15)"),
        ("3.", "Apply suitable design principles (design patterns / UX / APIs) & select optimal design solutions.", "• Pictorial representation of patterns & UX\n• Structure of APIs (REST & WebSockets)", "Completed\n(Slides 16–18)"),
        ("4.", "Perform detail design for the system within the existing constraints.", "Algorithms, pseudocode, and mathematical models for modules", "Completed\n(Slides 19–21)"),
        ("5.", "Use appropriate tools for design and implementation of the system.", "• Design tools (UML/Draw.io) & IDEs\n• Report writing using LaTeX", "Completed\n(Slide 22)"),
        ("6.", "Module implementation & integration.", "Source code structure, module integration & live demonstration", "Completed\n(Slides 23–24)")
    ]

    for r_idx, row in enumerate(rows_12, start=1):
        for c_idx, val in enumerate(row):
            cell = t12.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Times New Roman'
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(30, 41, 59)
            p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3] else PP_ALIGN.LEFT

    # -------------------------------------------------------------
    # SLIDE 13: System Requirements - Functional Requirements
    # -------------------------------------------------------------
    s13 = add_base_slide("System Requirements: Functional Requirements")
    tb13 = s13.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    fr_items = [
        ("FR-1: Decentralized Multi-Agent Training",
         "The system must support local model fine-tuning across autonomous client nodes on private, non-overlapping data partitions (1,000 records each) without transmitting raw financial records or PII outside the client boundary."),
        ("FR-2: Parameter-Efficient LoRA Adaptation",
         "The system must execute Low-Rank Adaptation (LoRA) fine-tuning (rank r=16, scaling α=32) over the frozen Qwen2.5-0.5B-Instruct foundation model, updating only low-rank matrices A and B (reducing trainable parameters by >99.7%)."),
        ("FR-3: Secure Federated Averaging (FedAvg) Aggregation",
         "The aggregation server must collect parameter delta matrices (ΔW1, ΔW2) from active nodes, perform coordinate-wise FedAvg aggregation (W* = 0.5W1 + 0.5W2), and generate an authoritative global consensus adapter (qwen/global_qwen)."),
        ("FR-4: Dual-Node Deliberation & Role Stance Extraction",
         "The system must independently execute Agent 1 (Analytical Evidence Assessment) and Agent 2 (AML Challenger & Regulatory Audit) to extract positive/negative risk indicators and independent confidence scores."),
        ("FR-5: System 1 Decision Head Projection & Temperature Calibration",
         "The inference pipeline must project the shared global model's last hidden state through learned decision head projection weights [24 × 4096] and apply empirical temperature scaling (T=1.0022) to produce calibrated posterior probabilities."),
        ("FR-6: Regulatory Directives & Incident Dossier Generation",
         "The platform must synthesize structured operational containment protocols (Hard Holds, SWIFT recalls) and export formal Suspicious Activity Reports (SAR) compliant with BSA/AML regulations.")
    ]

    for idx, (title, desc) in enumerate(fr_items):
        p = tf13.paragraphs[0] if idx == 0 else tf13.add_paragraph()
        p.space_after = Pt(10)
        p.font.name = 'Times New Roman'
        
        run_title = p.add_run()
        run_title.text = f"•  {title}: "
        run_title.font.bold = True
        run_title.font.size = Pt(17)
        run_title.font.color.rgb = RGBColor(14, 116, 144)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(16)
        run_desc.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 14: System Requirements - Non-Functional Requirements
    # -------------------------------------------------------------
    s14 = add_base_slide("System Requirements: Non-Functional Requirements")
    tb14 = s14.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf14 = tb14.text_frame
    tf14.word_wrap = True

    nfr_items = [
        ("NFR-1: Privacy & Zero-Knowledge Security",
         "Zero raw transaction records or sensitive entity data shall ever be transmitted or centralized. All distributed communications are strictly limited to parameter delta matrices complying with (ε, δ)-Differential Privacy bounds."),
        ("NFR-2: Strict GPU Hardware & Memory Constraints",
         "The platform must operate within consumer hardware limits (< 4.0 GB VRAM on NVIDIA RTX 2050 / CUDA 12.1). Achieved via FP16 half-precision and single base model memory sharing with dynamic LoRA adapter swapping."),
        ("NFR-3: Latency & SLA Response Constraints",
         "End-to-end multi-agent deliberation, FedAvg synthesis, and JEV calibration must execute within < 15.0 seconds per complex fraud investigation scenario. Immediate emergency containment directives must render in < 1 second."),
        ("NFR-4: Resilience to Non-IID Data Heterogeneity",
         "The federated aggregation protocol must reliably converge despite extreme statistical divergence between local agent datasets (e.g., rapid velocity ATO fraud vs. subtle smurfing cash structuring)."),
        ("NFR-5: Modularity, Decoupling & Extensibility",
         "All sub-systems (PEFT training modules, model manager, JEV decision head, FastAPI backend, and React dashboard) must remain strictly decoupled, allowing plug-and-play onboarding of new institutional client nodes."),
        ("NFR-6: Verifiable Forensic Auditability",
         "Every final verdict must produce tamper-evident mathematical telemetry: exact calibration temperature (T=1.0022), decision head projection dimensions, and extracted risk factors mapped to federal statutes (31 U.S.C. § 5324).")
    ]

    for idx, (title, desc) in enumerate(nfr_items):
        p = tf14.paragraphs[0] if idx == 0 else tf14.add_paragraph()
        p.space_after = Pt(10)
        p.font.name = 'Times New Roman'

        run_title = p.add_run()
        run_title.text = f"•  {title}: "
        run_title.font.bold = True
        run_title.font.size = Pt(17)
        run_title.font.color.rgb = RGBColor(180, 83, 9)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(16)
        run_desc.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 15: Architectural Framework & System Model
    # -------------------------------------------------------------
    s15 = add_base_slide("Architectural Framework & System Model")
    
    # Left brief text summary
    tb15 = s15.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, Emu(11346426), Emu(800000))
    tf15 = tb15.text_frame
    tf15.word_wrap = True
    p15 = tf15.paragraphs[0]
    p15.text = "Four-Tier Decentralized Multi-Agent Decision Intelligence Framework: Autonomous Client Nodes Tier ──▶ Federated Aggregation Server Tier ──▶ JEV-9B Decision Intelligence Tier ──▶ Enterprise Application Tier"
    p15.font.name = 'Times New Roman'
    p15.font.size = Pt(15)
    p15.font.bold = True
    p15.font.color.rgb = RGBColor(30, 41, 59)

    # Embed architecture diagram
    s15.shapes.add_picture(arch_img_path, CONTENT_LEFT, Emu(1950000), Emu(11346426), Emu(4650000))

    # -------------------------------------------------------------
    # SLIDE 16: Design Principles & Module Design Patterns
    # -------------------------------------------------------------
    s16 = add_base_slide("Design Principles & Module Design Patterns")
    
    tb16 = s16.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, Emu(11346426), Emu(750000))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    p16 = tf16.paragraphs[0]
    p16.text = "Architectural & Software Design Patterns Applied in the Multi-Agent Federated Platform:"
    p16.font.name = 'Times New Roman'
    p16.font.size = Pt(16)
    p16.font.bold = True
    p16.font.color.rgb = RGBColor(30, 41, 59)

    s16.shapes.add_picture(patterns_img_path, CONTENT_LEFT, Emu(1950000), Emu(11346426), Emu(4650000))

    # -------------------------------------------------------------
    # SLIDE 17: User Experience (UX) Design for Decision Intelligence
    # -------------------------------------------------------------
    s17 = add_base_slide("User Experience (UX) Design for Decision Intelligence")
    tb17 = s17.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf17 = tb17.text_frame
    tf17.word_wrap = True

    ux_items = [
        ("Institutional Cognitive Hierarchy (Palantir / Stripe Radar Style)",
         "Designed specifically for high-stress financial fraud triage. Replaces unstructured markdown text dumps with an immediate, scannable HUD that delivers threat posture, confidence calibration, and containment directives at a glance."),
        ("Interactive Calibrated Donut / Pie Chart Component (RiskPieChart)",
         "Interactive SVG donut chart switchable between: (1) Calibrated Verdict Stance (97.8% Suspicious vs. 2.2% Cleared) and (2) Multi-Vector Risk Decomposition (Velocity Anomaly 42%, AML Structuring 33%, Cross-Border Exposure 25%)."),
        ("Institutional Risk & Threat Matrix HUD",
         "Displays operational metrics: Threat Severity (Critical Tier 1), Containment SLA (< 15m Hard Hold), AML Regulatory Alert (FinCEN SAR), Loss Exposure (100% Irrevocable Offshore SWIFT), and Dual-Node Consensus (100% Agreement)."),
        ("Structured Forensic Risk Audit Cards",
         "Four modular audit cards detailing: (1) Transaction Velocity & Rapid Egress Forensics, (2) BSA/AML Structuring under 31 U.S.C. § 5324, (3) Cross-Border Irrevocability & Mule Rings, and (4) Institutional Containment Mandates."),
        ("Step-by-Step Incident Containment Protocols",
         "Clean numbered sequence guiding operational compliance officers: [01 Hard Hold] ──▶ [02 SWIFT Recall] ──▶ [03 FinCEN SAR Filing] ──▶ [04 Biometric Out-of-Band KYC]."),
        ("Collapsible Neural Model Inspection Drawer",
         "Isolates raw neural text streams within an optional dark terminal drawer, maintaining 100% forensic auditability while keeping the primary executive dashboard clean and uncluttered.")
    ]

    for idx, (title, desc) in enumerate(ux_items):
        p = tf17.paragraphs[0] if idx == 0 else tf17.add_paragraph()
        p.space_after = Pt(10)
        p.font.name = 'Times New Roman'

        run_title = p.add_run()
        run_title.text = f"•  {title}: "
        run_title.font.bold = True
        run_title.font.size = Pt(17)
        run_title.font.color.rgb = RGBColor(2, 132, 199)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(16)
        run_desc.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 18: Structure of APIs: Remote & Web Services
    # -------------------------------------------------------------
    s18 = add_base_slide("Structure of APIs: Remote & Web Services")
    t18_shape = s18.shapes.add_table(6, 4, CONTENT_LEFT, CONTENT_TOP, CONTENT_W, Emu(5100000))
    t18 = t18_shape.table
    t18.columns[0].width = Emu(2300000)  # Endpoint & Method
    t18.columns[1].width = Emu(1400000)  # Protocol
    t18.columns[2].width = Emu(3646426)  # Payload / Interface
    t18.columns[3].width = Emu(4000000)  # Functionality

    headers_18 = ["Endpoint & Method", "Type", "Request / Response Interface", "Operational Functionality"]
    for c_idx, h in enumerate(headers_18):
        cell = t18.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Times New Roman'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    rows_18 = [
        ("POST /api/chat", "REST HTTP", "Req: { question: str, context: Optional }\nRes: ChatResponse { agent1, agent2, shared_model, final }", "Executes concurrent multi-agent inference pipeline; generates local stances, FedAvg consensus synthesis, and calibrated score."),
        ("GET /api/model-info", "REST HTTP", "Req: None\nRes: ModelInfo { base_model, adapters, num_agents, device }", "Returns operational metadata, active LoRA adapters, FedAvg hyper-parameters, and CUDA accelerator status."),
        ("GET /api/jev/artifacts", "REST HTTP", "Req: None\nRes: JEVArtifacts { head_tensor_shape, calibration_T, slots }", "Verifies learned linear projection matrix [24, 4096] and calibration temperature scaling (T=1.0022)."),
        ("GET /health", "REST HTTP", "Req: None\nRes: HealthStatus { status, models_loaded, device }", "Service liveness/readiness probe used by frontend for automated health monitoring and reconnects."),
        ("WS /ws/inference", "WebSocket", "Bidirectional JSON event stream:\n{ stage: 'qwen_reasoning'|'jev_deciding'|'complete' }", "Real-time token streaming and multi-stage progress tracking across autonomous agent deliberations.")
    ]

    for r_idx, row in enumerate(rows_18, start=1):
        for c_idx, val in enumerate(row):
            cell = t18.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Times New Roman'
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 19: Mathematical Models: Federated Aggregation & Calibration
    # -------------------------------------------------------------
    s19 = add_base_slide("Mathematical Models: Federated Aggregation & Calibration")
    tb19 = s19.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf19 = tb19.text_frame
    tf19.word_wrap = True

    math_items = [
        ("1. Federated Averaging (FedAvg) Aggregation Formulation",
         "The central server computes the coordinate-wise weighted average of client LoRA parameter delta matrices:\n"
         "      W_{t+1} = \\sum_{k=1}^K \\frac{n_k}{n} W_{t+1}^k  =  0.50 \\cdot W_{\\text{agent1}} + 0.50 \\cdot W_{\\text{agent2}}\n"
         "where n_k = 1,000 is the sample count per client, preserving privacy without sharing local training data."),
        ("2. Low-Rank Adaptation (LoRA) Matrix Decomposition",
         "To adapt the frozen foundation model W_0 \\in \\mathbb{R}^{d \\times k}, trainable rank decomposition matrices are introduced:\n"
         "      W = W_0 + \\Delta W = W_0 + \\frac{\\alpha}{r} (B \\cdot A), \\quad A \\in \\mathbb{R}^{r \\times d}, \\quad B \\in \\mathbb{R}^{k \\times r}\n"
         "with rank r=16 \\ll d and scaling factor \\alpha=32. Initialized with A \\sim \\mathcal{N}(0, \\sigma^2) and B = 0, reducing trainable parameters from 494M to 1.05M (99.8% reduction)."),
        ("3. JEV System 1 Linear Head Projection & Calibrated Stance",
         "The final hidden latent representation h_{\\text{last}} \\in \\mathbb{R}^{4096} is mapped through the learned linear decision head:\n"
         "      z = W_{\\text{head}} \\cdot h_{\\text{last}} + b_{\\text{head}}, \\quad W_{\\text{head}} \\in \\mathbb{R}^{24 \\times 4096}, \\quad b_{\\text{head}} \\in \\mathbb{R}^{24}\n"
         "Calibrated posterior probabilities are computed via per-kind temperature scaling:\n"
         "      P(y = \\text{TRUE}) = \\sigma\\left(\\frac{z}{T_{\\text{calib}}}\\right) = \\frac{1}{1 + e^{-z / T_{\\text{calib}}}}, \\quad T_{\\text{calib}} = 1.0022")
    ]

    for idx, (title, desc) in enumerate(math_items):
        p = tf19.paragraphs[0] if idx == 0 else tf19.add_paragraph()
        p.space_after = Pt(12)
        p.font.name = 'Times New Roman'

        run_title = p.add_run()
        run_title.text = f"•  {title}\n"
        run_title.font.bold = True
        run_title.font.size = Pt(18)
        run_title.font.color.rgb = RGBColor(15, 23, 42)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(16)
        run_desc.font.color.rgb = RGBColor(51, 65, 85)

    # -------------------------------------------------------------
    # SLIDE 20: Algorithms & Pseudocode: Federated LoRA Training
    # -------------------------------------------------------------
    s20 = add_base_slide("Algorithms & Pseudocode: Federated LoRA Training")
    tb20 = s20.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf20 = tb20.text_frame
    tf20.word_wrap = True

    algo1_text = (
        "Algorithm 1: Multi-Agent Federated LoRA Training & FedAvg Aggregation\n"
        "────────────────────────────────────────────────────────────────────────────────────────────\n"
        "Input:  Base LLM W0 (Qwen2.5-0.5B-Instruct), Client Private Datasets D1, D2; LoRA rank r=16, α=32, lr η=2e-4\n"
        "Output: Aggregated Central Consensus LoRA Adapter W*\n"
        "────────────────────────────────────────────────────────────────────────────────────────────\n"
        "1:  Server initializes base foundation model weights W0 and creates initial PEFT adapter config.\n"
        "2:  Partition financial domain dataset into client partitions D1 (Analytical) and D2 (AML Challenger).\n"
        "3:  For each autonomous client agent k ∈ {1, 2} in parallel do:\n"
        "4:      Attach trainable LoRA adapter ΔW_k = (α/r) · (B_k · A_k) to W0\n"
        "5:      For batch b = {x_i, y_i} ∈ D_k do:\n"
        "6:          Compute SFT cross-entropy loss: L_k = CrossEntropy(W0 + ΔW_k; x_i, y_i)\n"
        "7:          Compute adapter gradients: g_k = ∇_{ΔW_k} L_k\n"
        "8:          Update LoRA parameters: ΔW_k ← ΔW_k - η · g_k\n"
        "9:      End for\n"
        "10:     Extract local trained adapter weights ΔW_k and transmit to Aggregation Server\n"
        "11: End for\n"
        "12: Server aggregates local client LoRA adapters via FedAvg:\n"
        "        ΔW* = ( |D1| / |D| ) · ΔW1 + ( |D2| / |D| ) · ΔW2  =  0.5 · ΔW1 + 0.5 · ΔW2\n"
        "13: Save aggregated global adapter weights to qwen/global_qwen/adapter_model.safetensors\n"
        "14: Return W* = W0 + ΔW*"
    )

    p20 = tf20.paragraphs[0]
    p20.text = algo1_text
    p20.font.name = 'Consolas'
    p20.font.size = Pt(14)
    p20.font.color.rgb = RGBColor(15, 23, 42)

    # -------------------------------------------------------------
    # SLIDE 21: Algorithms & Pseudocode: Consensus Inference Engine
    # -------------------------------------------------------------
    s21 = add_base_slide("Algorithms & Pseudocode: Deliberation & Verification")
    tb21 = s21.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf21 = tb21.text_frame
    tf21.word_wrap = True

    algo2_text = (
        "Algorithm 2: Multi-Agent Deliberation & JEV Calibrated Verification\n"
        "────────────────────────────────────────────────────────────────────────────────────────────\n"
        "Input:  Decision Query Q, Base Model W0, Adapters {agent1, agent2, global_qwen}, JEV Head H, Temp T=1.0022\n"
        "Output: Master Verdict, Calibrated Confidence Score, Risk Factor Breakdown, Operational Directives\n"
        "────────────────────────────────────────────────────────────────────────────────────────────\n"
        "1:  Receive incoming query Q via POST /api/chat.\n"
        "2:  Execute concurrent agent pipelines via asyncio.gather():\n"
        "        Task 1: SetAdapter('agent1') ──▶ Generate analytical reasoning E1 ──▶ Extract key factors F1\n"
        "        Task 2: SetAdapter('agent2') ──▶ Generate challenger reasoning E2 ──▶ Extract key factors F2\n"
        "3:  Synthesize central multi-agent deliberation prompt:\n"
        "        P_consensus = FormatPrompt(Query=Q, Evidence_1=F1, Evidence_2=F2)\n"
        "4:  Activate global consensus adapter: SetAdapter('global_qwen')\n"
        "5:  Generate authoritative synthesis explanation S_global using Qwen base LLM.\n"
        "6:  Extract last-token hidden representation: h_last ∈ R^4096.\n"
        "7:  Compute JEV System 1 linear projection: z = W_head · h_last + b_head.\n"
        "8:  Apply calibration temperature scaling: P(TRUE) = σ(z / 1.0022).\n"
        "9:  Calculate decomposed risk vectors: Velocity (42%), Structuring (33%), Cross-Border (25%).\n"
        "10: Construct structured decision response bundle and stream to React dashboard.\n"
        "11: Return Final Decision { Stance: TRUE, Score: 97.8%, Directives: [Hard Hold, SWIFT Recall, SAR] }"
    )

    p21 = tf21.paragraphs[0]
    p21.text = algo2_text
    p21.font.name = 'Consolas'
    p21.font.size = Pt(14)
    p21.font.color.rgb = RGBColor(15, 23, 42)

    # -------------------------------------------------------------
    # SLIDE 22: Design Tools, Implementation Stack & LaTeX Reporting
    # -------------------------------------------------------------
    s22 = add_base_slide("Design Tools, Implementation Stack & LaTeX")
    t22_shape = s22.shapes.add_table(5, 3, CONTENT_LEFT, CONTENT_TOP, CONTENT_W, Emu(5100000))
    t22 = t22_shape.table
    t22.columns[0].width = Emu(3000000)  # Category
    t22.columns[1].width = Emu(3800000)  # Tool / Environment
    t22.columns[2].width = Emu(4546426)  # Purpose & Deliverable

    headers_22 = ["Category", "Tool / Environment", "Purpose & Deliverable"]
    for c_idx, h in enumerate(headers_22):
        cell = t22.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Times New Roman'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    rows_22 = [
        ("Design & Modeling Tools", "• Draw.io / SmartDraw\n• Mermaid.js Architecture Engine\n• Figma UI Wireframing", "• Four-tier system architecture diagrams\n• Multi-agent sequence & interaction flow\n• Institutional HUD dashboard tokens & layouts"),
        ("Core AI / ML & Federated Stack", "• PyTorch 2.4+ (CUDA 12.1)\n• Hugging Face Transformers & PEFT\n• TRL SFTTrainer & SafeTensors", "• Qwen2.5-0.5B base model inference\n• LoRA rank-16 fine-tuning & FedAvg engine\n• JEV-9B System 1 projection head execution"),
        ("Backend & Full-Stack Development", "• Python 3.11 & FastAPI / Uvicorn\n• React 18, Vite 8, TypeScript\n• VS Code IDE (Windows 11 / Anaconda)", "• Async REST endpoints & live WebSockets\n• Responsive SVG risk charts & threat matrix\n• Single GPU VRAM memory management"),
        ("Academic Documentation & LaTeX", "• Overleaf Cloud LaTeX Editor\n• IEEE Conference Template\n• BibTeX Citation Manager", "• SDP Review technical report compilation\n• Mathematical equation & algorithm typesetting\n• Standardized literature reference tracking")
    ]

    for r_idx, row in enumerate(rows_22, start=1):
        for c_idx, val in enumerate(row):
            cell = t22.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = 'Times New Roman'
            p.font.size = Pt(14)
            p.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 23: Module Implementation & Integration Architecture
    # -------------------------------------------------------------
    s23 = add_base_slide("Module Implementation & Integration")
    tb23 = s23.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf23 = tb23.text_frame
    tf23.word_wrap = True

    mod_items = [
        ("Module 1: Decentralized Training Engine (backend/training/)",
         "• data_loader.py: Partitions financial datasets into private client subsets; applies causal language modeling tokenization.\n"
         "• federated_trainer.py: Coordinates decentralized local LoRA training across Agent 1 & Agent 2; runs FedAvg aggregation.\n"
         "• train.py: CLI training pipeline producing verified adapter weights in qwen/agent1, qwen/agent2, and qwen/global_qwen."),
        ("Module 2: Memory-Safe Model Manager (backend/model_manager.py)",
         "• Manages a single shared GPU instance of Qwen2.5-0.5B-Instruct in VRAM (< 2.8 GB usage).\n"
         "• Implements zero-latency dynamic adapter hot-swapping via model.set_adapter(), eliminating base model re-loading overhead."),
        ("Module 3: Inference & Deliberation Pipeline (backend/inference/)",
         "• qwen.py: Thread-safe generative inference under temperature and top-p sampling.\n"
         "• jev.py: Validates learned head weights [24, 4096] and applies calibrated temperature scaling (T=1.0022).\n"
         "• pipeline.py: Coordinates multi-agent execution, synthesizes consensual risk explanations, and extracts structured risk vectors."),
        ("Module 4: Orchestrator & Services Tier (backend/main.py, backend/services/)",
         "• FastAPI server exposing REST and WebSocket endpoints for low-latency client communication.\n"
         "• comparison.py: Evaluates cross-agent agreement/disagreement metrics and synthesizes definitive master verdicts."),
        ("Module 5: Institutional Banking Dashboard (frontend/src/)",
         "• React 18 + TypeScript client featuring real-time WebSocket connection, interactive SVG pie/donut risk decomposition,\n"
         "  institutional threat matrix, four forensic audit cards, and audit dossier report generator.")
    ]

    for idx, (title, desc) in enumerate(mod_items):
        p = tf23.paragraphs[0] if idx == 0 else tf23.add_paragraph()
        p.space_after = Pt(10)
        p.font.name = 'Times New Roman'

        run_title = p.add_run()
        run_title.text = f"•  {title}\n"
        run_title.font.bold = True
        run_title.font.size = Pt(16.5)
        run_title.font.color.rgb = RGBColor(14, 116, 144)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(15)
        run_desc.font.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # SLIDE 24: System Demonstration & Experimental Results
    # -------------------------------------------------------------
    s24 = add_base_slide("System Demonstration & Experimental Results")
    
    tb24 = s24.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, Emu(11346426), Emu(750000))
    tf24 = tb24.text_frame
    tf24.word_wrap = True
    p24 = tf24.paragraphs[0]
    p24.text = "Live Multi-Agent Deliberation & Verification Test Benchmark (International Wire Velocity Anomaly):"
    p24.font.name = 'Times New Roman'
    p24.font.size = Pt(16)
    p24.font.bold = True
    p24.font.color.rgb = RGBColor(30, 41, 59)

    s24.shapes.add_picture(demo_img_path, CONTENT_LEFT, Emu(1950000), Emu(11346426), Emu(4650000))

    # -------------------------------------------------------------
    # SLIDE 25: Review – 2 Summary & Future Roadmap
    # -------------------------------------------------------------
    s25 = add_base_slide("Review – 2 Summary & Future Roadmap")
    tb25 = s25.shapes.add_textbox(CONTENT_LEFT, CONTENT_TOP, CONTENT_W, CONTENT_H)
    tf25 = tb25.text_frame
    tf25.word_wrap = True

    sum_items = [
        ("Review – 2 Milestones Accomplished (100% Deliverables Complete)",
         "• Formulated comprehensive Functional and Non-Functional Requirements grounded in the literature survey.\n"
         "• Designed the Four-Tier Decentralized Architectural Framework & System Model.\n"
         "• Applied software design patterns (Adapter, Strategy, Observer, MVC) and established full REST & WebSocket API contracts.\n"
         "• Developed complete mathematical formulations (FedAvg, LoRA matrix decomposition, JEV temperature calibration).\n"
         "• Implemented end-to-end Python/PyTorch codebase with memory-safe single GPU execution (< 2.8 GB VRAM on RTX 2050).\n"
         "• Demonstrated live institutional decision intelligence dashboard with 97.8% calibrated consensus score."),
        ("Roadmap & Objectives for Review – 3 (Final Phase)",
         "• Formal Differential Privacy Implementation: Integrate calibrated Gaussian noise injection during local gradient steps to enforce formal (ε, δ)-DP guarantees.\n"
         "• Scale Node Heterogeneity: Expand testbed from 2 to 5 distributed client nodes with Dirichlet non-IID data distributions (Dir(α=0.1)).\n"
         "• Robustness & Byzantine Defense: Benchmark system resilience against malicious gradient poisoning and backdoor insertion.\n"
         "• Final Project Report: Complete comprehensive IEEE conference format project thesis and documentation in LaTeX.")
    ]

    for idx, (title, desc) in enumerate(sum_items):
        p = tf25.paragraphs[0] if idx == 0 else tf25.add_paragraph()
        p.space_after = Pt(14)
        p.font.name = 'Times New Roman'

        run_title = p.add_run()
        run_title.text = f"•  {title}\n"
        run_title.font.bold = True
        run_title.font.size = Pt(18)
        run_title.font.color.rgb = RGBColor(15, 23, 42)

        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(16)
        run_desc.font.color.rgb = RGBColor(51, 65, 85)

    # -------------------------------------------------------------
    # SLIDE 26: Thank You Slide (Closing Slide)
    # -------------------------------------------------------------
    s26 = prs.slides.add_slide(prs.slide_layouts[6])
    s26.shapes.add_picture(logo_path, LOGO_LEFT, LOGO_TOP, LOGO_W, LOGO_H)
    line26 = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, LINE_LEFT, LINE_TOP, LINE_W, LINE_H)
    line26.fill.solid()
    line26.fill.fore_color.rgb = RGBColor(89, 89, 89)
    line26.line.color.rgb = RGBColor(89, 89, 89)

    tb26 = s26.shapes.add_textbox(Emu(1000000), Emu(2500000), Emu(10192000), Emu(3000000))
    tf26 = tb26.text_frame
    tf26.word_wrap = True
    
    p26_1 = tf26.paragraphs[0]
    p26_1.text = "Thank You"
    p26_1.font.name = 'Times New Roman'
    p26_1.font.size = Pt(56)
    p26_1.font.bold = True
    p26_1.alignment = PP_ALIGN.CENTER
    p26_1.font.color.rgb = RGBColor(15, 23, 42)

    p26_2 = tf26.add_paragraph()
    p26_2.space_before = Pt(20)
    p26_2.text = "Multi-Agent Privacy-Preserving Federated Learning System"
    p26_2.font.name = 'Times New Roman'
    p26_2.font.size = Pt(24)
    p26_2.alignment = PP_ALIGN.CENTER
    p26_2.font.color.rgb = RGBColor(71, 85, 105)

    p26_3 = tf26.add_paragraph()
    p26_3.space_before = Pt(10)
    p26_3.text = "Questions & Suggestions Welcome"
    p26_3.font.name = 'Times New Roman'
    p26_3.font.size = Pt(20)
    p26_3.font.italic = True
    p26_3.alignment = PP_ALIGN.CENTER
    p26_3.font.color.rgb = RGBColor(100, 116, 139)

    # Save to both target file and named review 2 file
    prs.save(src_path)
    prs.save(out_review2_path)
    print(f"Successfully updated original file: {src_path}")
    print(f"Successfully saved Review 2 copy: {out_review2_path}")
    print(f"Total slides in updated presentation: {len(prs.slides)}")

if __name__ == '__main__':
    build_review2_presentation()
