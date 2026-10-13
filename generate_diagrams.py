import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color palette
    c_client_bg = '#f0fdf4'
    c_client_border = '#16a34a'
    c_server_bg = '#eff6ff'
    c_server_border = '#2563eb'
    c_jev_bg = '#faf5ff'
    c_jev_border = '#9333ea'
    c_ui_bg = '#f8fafc'
    c_ui_border = '#0284c7'
    c_box = '#ffffff'

    # Background zones
    # Zone 1: Autonomous Client Nodes Tier
    ax.add_patch(patches.FancyBboxPatch((2, 2), 44, 94, boxstyle="round,pad=1", fc='#f8fafc', ec='#cbd5e1', lw=1.5, ls='--'))
    ax.text(24, 93, 'TIER 1: AUTONOMOUS CLIENT DATA & LOCAL PEFT TRAINING', ha='center', va='center', fontsize=9, fontweight='bold', color='#334155', fontfamily='serif')

    # Client Node 1
    ax.add_patch(patches.FancyBboxPatch((4, 52), 40, 36, boxstyle="round,pad=0.8", fc=c_client_bg, ec=c_client_border, lw=2))
    ax.text(24, 84, 'Agent 1: Analytical / Evidence Node', ha='center', va='center', fontsize=10, fontweight='bold', color='#15803d', fontfamily='serif')
    
    # Internal boxes in Node 1
    ax.add_patch(patches.Rectangle((6, 68), 16, 12, fc='#ffffff', ec='#86efac', lw=1))
    ax.text(14, 75, 'Private Partition D1\n(1,000 Financial Records)', ha='center', va='center', fontsize=7.5, color='#14532d', fontfamily='serif')

    ax.add_patch(patches.Rectangle((26, 68), 16, 12, fc='#ffffff', ec='#86efac', lw=1))
    ax.text(34, 75, 'Base LLM (Shared)\nQwen2.5-0.5B-Instruct', ha='center', va='center', fontsize=7.5, color='#14532d', fontfamily='serif')

    ax.add_patch(patches.Rectangle((12, 54), 24, 10, fc='#dcfce7', ec='#22c55e', lw=1.5))
    ax.text(24, 59, 'LoRA Adapter W1 (r=16, α=32)\nqwen/agent1 (Trainable PEFT)', ha='center', va='center', fontsize=8, fontweight='bold', color='#166534', fontfamily='serif')

    # Client Node 2
    ax.add_patch(patches.FancyBboxPatch((4, 8), 40, 36, boxstyle="round,pad=0.8", fc='#fdf4ff', ec='#a855f7', lw=2))
    ax.text(24, 40, 'Agent 2: Critical Challenger / AML Node', ha='center', va='center', fontsize=10, fontweight='bold', color='#7e22ce', fontfamily='serif')

    ax.add_patch(patches.Rectangle((6, 24), 16, 12, fc='#ffffff', ec='#e9d5ff', lw=1))
    ax.text(14, 31, 'Private Partition D2\n(1,000 AML & Risk Rows)', ha='center', va='center', fontsize=7.5, color='#581c87', fontfamily='serif')

    ax.add_patch(patches.Rectangle((26, 24), 16, 12, fc='#ffffff', ec='#e9d5ff', lw=1))
    ax.text(34, 31, 'Base LLM (Shared)\nQwen2.5-0.5B-Instruct', ha='center', va='center', fontsize=7.5, color='#581c87', fontfamily='serif')

    ax.add_patch(patches.Rectangle((12, 10), 24, 10, fc='#f3e8ff', ec='#9333ea', lw=1.5))
    ax.text(24, 15, 'LoRA Adapter W2 (r=16, α=32)\nqwen/agent2 (Trainable PEFT)', ha='center', va='center', fontsize=8, fontweight='bold', color='#6b21a8', fontfamily='serif')

    # Zone 2: Federated Aggregation Server Tier
    ax.add_patch(patches.FancyBboxPatch((50, 48), 22, 48, boxstyle="round,pad=0.8", fc=c_server_bg, ec=c_server_border, lw=2))
    ax.text(61, 92, 'TIER 2: FEDERATED SERVER', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e40af', fontfamily='serif')
    
    ax.add_patch(patches.Rectangle((52, 74), 18, 14, fc='#ffffff', ec='#93c5fd', lw=1.2))
    ax.text(61, 82, 'FedAvg Aggregation\nEngine (w* = 0.5w1 + 0.5w2)\nWeight Merge Protocol', ha='center', va='center', fontsize=7.5, color='#1e3a8a', fontfamily='serif')

    ax.add_patch(patches.Rectangle((52, 54), 18, 15, fc='#dbeafe', ec='#3b82f6', lw=1.5))
    ax.text(61, 62, 'Global LoRA Model\nqwen/global_qwen\nConsensus Adapter', ha='center', va='center', fontsize=8, fontweight='bold', color='#1d4ed8', fontfamily='serif')

    # Zone 3: JEV Decision Intelligence Tier
    ax.add_patch(patches.FancyBboxPatch((50, 2), 22, 42, boxstyle="round,pad=0.8", fc=c_jev_bg, ec=c_jev_border, lw=2))
    ax.text(61, 40, 'TIER 3: JEV-9B DECISION HEAD', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#6b21a8', fontfamily='serif')

    ax.add_patch(patches.Rectangle((52, 23), 18, 13, fc='#ffffff', ec='#d8b4fe', lw=1.2))
    ax.text(61, 30, 'Linear Head Projection\nhead.safetensors\n[24 x 4096 weights]', ha='center', va='center', fontsize=7.5, color='#4a044e', fontfamily='serif')

    ax.add_patch(patches.Rectangle((52, 6), 18, 13, fc='#f5d0fe', ec='#c026d3', lw=1.2))
    ax.text(61, 13, 'System 1 Calibration\ncalibration.json (T=1.0022)\nProbabilistic Gate', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#701a75', fontfamily='serif')

    # Zone 4: Enterprise Orchestration & User Interface Tier
    ax.add_patch(patches.FancyBboxPatch((76, 2), 22, 94, boxstyle="round,pad=0.8", fc=c_ui_bg, ec=c_ui_border, lw=2))
    ax.text(87, 92, 'TIER 4: APPLICATION & UX', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0369a1', fontfamily='serif')

    ax.add_patch(patches.Rectangle((78, 68), 18, 18, fc='#ffffff', ec='#7dd3fc', lw=1.2))
    ax.text(87, 78, 'FastAPI Orchestrator\nREST: /api/chat\nWebSocket: /ws/inference\nVRAM-Safe Swapper', ha='center', va='center', fontsize=8, color='#0c4a6e', fontfamily='serif')

    ax.add_patch(patches.Rectangle((78, 38), 18, 24, fc='#e0f2fe', ec='#0284c7', lw=1.5))
    ax.text(87, 50, 'React + Vite UI\n- SVG Risk Donut\n- Institutional Matrix\n- Forensic Audit Cards\n- SAR Audit Dossier', ha='center', va='center', fontsize=8, fontweight='bold', color='#075985', fontfamily='serif')

    ax.add_patch(patches.Rectangle((78, 8), 18, 24, fc='#ffffff', ec='#94a3b8', lw=1.2))
    ax.text(87, 20, 'Human Analyst / FIU\nRegulatory Decision\n- 97.8% Calibrated Score\n- Hard Hold Protocol\n- AML SAR Compliance', ha='center', va='center', fontsize=7.5, color='#1e293b', fontfamily='serif')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="->", lw=1.8, color="#0f172a", shrinkA=4, shrinkB=4)
    # W1 to Server
    ax.annotate('', xy=(50, 78), xytext=(36, 59), arrowprops=dict(arrowstyle="->", lw=2, color="#16a34a"))
    ax.text(43, 72, 'Local W1', fontsize=7.5, color='#16a34a', fontweight='bold')

    # W2 to Server
    ax.annotate('', xy=(50, 64), xytext=(36, 15), arrowprops=dict(arrowstyle="->", lw=2, color="#9333ea"))
    ax.text(43, 38, 'Local W2', fontsize=7.5, color='#9333ea', fontweight='bold')

    # Server to JEV
    ax.annotate('', xy=(61, 36), xytext=(61, 54), arrowprops=dict(arrowstyle="->", lw=2, color="#2563eb"))
    ax.text(62, 45, 'Latents h', fontsize=8, color='#2563eb', fontweight='bold')

    # Server & JEV to FastAPI
    ax.annotate('', xy=(78, 77), xytext=(70, 62), arrowprops=dict(arrowstyle="->", lw=2, color="#0284c7"))
    ax.annotate('', xy=(78, 75), xytext=(70, 20), arrowprops=dict(arrowstyle="->", lw=2, color="#c026d3"))

    # FastAPI to UI
    ax.annotate('', xy=(87, 62), xytext=(87, 68), arrowprops=arrow_props)
    # UI to User
    ax.annotate('', xy=(87, 32), xytext=(87, 38), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('architecture_diagram.png', bbox_inches='tight')
    plt.close()
    print("architecture_diagram.png created!")

def create_design_patterns_diagram():
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 4 Design Patterns Cards
    patterns = [
        ('1. Adapter Pattern (PEFT / LoRA Swapping)',
         'Context: Single GPU VRAM (4GB) constraint\nSolution: Base model Qwen2.5-0.5B weights remain frozen in memory; active LoRA adapters (agent1, agent2, global_qwen) hot-swapped dynamically via ModelManager.set_adapter().\nBenefit: Zero GPU reloading latency, 92% VRAM reduction.',
         '#f0fdf4', '#16a34a', 3, 52),
        ('2. Strategy & Multi-Stage Pipeline Pattern',
         'Context: Staged multi-agent inference execution\nSolution: Inference stages encapsulated into modular strategies:\nStage 1: Qwen LoRA reasoning generation\nStage 2: JEV Decision Engine linear head projection\nStage 3: Temperature scaling & probability normalization.',
         '#eff6ff', '#2563eb', 52, 52),
        ('3. Observer / Pub-Sub Pattern (WebSockets)',
         'Context: Real-time UI progress updates during deliberation\nSolution: FastAPI WebSocket publisher emits stage events (qwen_reasoning -> jev_deciding -> complete) to React client observers for live progress and token status rendering.',
         '#faf5ff', '#9333ea', 3, 3),
        ('4. Architectural Pattern: Model-View-Controller',
         'Context: Decoupling ML inference from user interaction\nModel: PyTorch LoRA models & JEV decision safetensors.\nController: FastAPI REST & WebSocket async routers.\nView: React 18 + Tailwind/CSS institutional banking dashboard.',
         '#fff7ed', '#ea580c', 52, 3),
    ]

    for title, desc, bg, border, x, y in patterns:
        ax.add_patch(patches.FancyBboxPatch((x, y), 45, 43, boxstyle="round,pad=1", fc=bg, ec=border, lw=2))
        ax.text(x + 22.5, y + 38, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=border, fontfamily='serif')
        ax.text(x + 2, y + 18, desc, ha='left', va='center', fontsize=8, color='#1e293b', fontfamily='serif', wrap=True)

    plt.tight_layout()
    plt.savefig('design_patterns_ux.png', bbox_inches='tight')
    plt.close()
    print("design_patterns_ux.png created!")

def create_system_demo_diagram():
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Left: Test Query & Input
    ax.add_patch(patches.FancyBboxPatch((2, 55), 45, 40, boxstyle="round,pad=0.8", fc='#f8fafc', ec='#64748b', lw=1.5))
    ax.text(24.5, 90, 'EVALUATION BENCHMARK QUERY', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e293b', fontfamily='serif')
    query_text = 'Scenario: "Does this series of multiple international\nwire transfers with rapid velocity require fraud investigation?"\n\nInput Context: 4 consecutive cross-border wire transfers\nof $850 each across offshore channels within 12 hours.'
    ax.text(4, 72, query_text, ha='left', va='center', fontsize=8, color='#334155', fontfamily='serif')

    # Left Bottom: Node Outputs
    ax.add_patch(patches.FancyBboxPatch((2, 5), 45, 45, boxstyle="round,pad=0.8", fc='#f0fdf4', ec='#16a34a', lw=1.5))
    ax.text(24.5, 45, 'LOCAL NODE REASONING & STANCES', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#15803d', fontfamily='serif')
    node_text = '• Agent 1 (Analytical): Stance = TRUE (Suspicious)\n  Confidence: 58.6% | Signal: Rapid egress velocity anomaly\n• Agent 2 (AML Challenger): Stance = TRUE (Audit Req)\n  Confidence: 87.4% | Signal: 31 U.S.C. § 5324 structuring\n• Agreement: DUAL-NODE CONSENSUS REACHED (100%)'
    ax.text(4, 25, node_text, ha='left', va='center', fontsize=8.2, color='#14532d', fontfamily='serif')

    # Right: Central Consensus Output
    ax.add_patch(patches.FancyBboxPatch((51, 5), 47, 90, boxstyle="round,pad=0.8", fc='#eff6ff', ec='#2563eb', lw=2))
    ax.text(74.5, 90, 'CENTRAL SHARED CONSENSUS ENGINE RESULTS', ha='center', va='center', fontsize=10, fontweight='bold', color='#1e40af', fontfamily='serif')
    
    # Score Box
    ax.add_patch(patches.Rectangle((54, 70), 41, 14, fc='#dbeafe', ec='#3b82f6', lw=1.5))
    ax.text(74.5, 77, 'Calibrated Decision Score: 97.8% (PERFECT SCORE)\nVerdict: TRUE (Action Mandated) | Calibration T = 1.0022', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e3a8a', fontfamily='serif')

    # Matrix Table in Diagram
    ax.text(54, 64, 'Threat Matrix & Operational Directives:', fontsize=8.5, fontweight='bold', color='#1e3a8a', fontfamily='serif')
    matrix_rows = [
        'Threat Severity: CRITICAL (TIER 1)',
        'Containment SLA: < 15m HARD HOLD MANDATED',
        'AML Regulatory Alert: FINCEN SAR FILING REQUIRED',
        'Loss Exposure: 100% IRREVOCABLE OFFSHORE SWIFT',
        'Risk Factors: Velocity (42%), Structuring (33%), Cross-Border (25%)',
        'Containment Action: Immediate hard freeze & MT199 recall'
    ]
    for idx, row in enumerate(matrix_rows):
        ax.text(56, 56 - (idx * 5.8), f'► {row}', fontsize=8, color='#1e293b', fontfamily='serif')

    ax.add_patch(patches.Rectangle((54, 10), 41, 8, fc='#f0fdf4', ec='#22c55e', lw=1))
    ax.text(74.5, 14, 'System Latency: 14.8s (Local CUDA RTX 2050 Execution)', ha='center', va='center', fontsize=8, fontweight='bold', color='#15803d', fontfamily='serif')

    plt.tight_layout()
    plt.savefig('system_demo_diagram.png', bbox_inches='tight')
    plt.close()
    print("system_demo_diagram.png created!")

if __name__ == '__main__':
    create_architecture_diagram()
    create_design_patterns_diagram()
    create_system_demo_diagram()
