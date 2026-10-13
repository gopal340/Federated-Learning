import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_main_blocks_diagram():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0)  # top to bottom flow
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    # Color palette
    c_blue = '#2563eb'
    c_blue_bg = '#eff6ff'
    c_green = '#16a34a'
    c_green_bg = '#f0fdf4'
    c_purple = '#9333ea'
    c_purple_bg = '#faf5ff'
    c_orange = '#ea580c'
    c_orange_bg = '#fff7ed'
    c_slate = '#475569'
    c_slate_bg = '#f8fafc'

    # Title
    ax.text(50, 6, "HIGH-LEVEL SYSTEM ARCHITECTURE", ha='center', va='center', fontsize=16, fontweight='bold', color='#0f172a')
    ax.text(50, 10, "Federated Multi-Agent Qwen + JEV Decision Pipeline", ha='center', va='center', fontsize=10, color='#64748b')

    # Helper function for blocks
    def draw_block(x, y, w, h, title, subtitle, bg, border, title_color='#0f172a'):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.5,rounding_size=1.0",
            fc=bg, ec=border, lw=2.0
        )
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 - 2, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_color)
        if subtitle:
            ax.text(x + w/2, y + h/2 + 3.5, subtitle, ha='center', va='center', fontsize=8.5, color='#475569')

    # Connecting arrow helper
    def draw_arrow(x1, y1, x2, y2, color='#64748b', lw=2.0, label=None):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.7", color=color, lw=lw)
        )
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 - 1.5, label, ha='center', va='center', fontsize=8, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.2", fc='#ffffff', ec=color, lw=1))

    # 1. Input Block (Top)
    draw_block(30, 16, 40, 11, "1. USER QUERY / TRANSACTION DATA", "Financial Transaction Context & Wire Details", c_slate_bg, c_slate, '#1e293b')

    # Arrow to Agent Layer
    draw_arrow(50, 27, 50, 34, c_slate)

    # 2. Parallel Federated Agent Blocks (Middle)
    # Background enclosure for Agent Layer
    enc = patches.FancyBboxPatch(
        (4, 34), 92, 23,
        boxstyle="round,pad=0.8,rounding_size=1.2",
        fc='#f8fafc', ec='#cbd5e1', lw=1.5, ls='--'
    )
    ax.add_patch(enc)
    ax.text(50, 37.5, "2. FEDERATED MULTI-AGENT REASONING LAYER", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')

    draw_block(6, 41, 26, 13, "AGENT 1: FRAUD", "Qwen LoRA (qwen/agent1)\nVelocity & Rail Analysis", c_green_bg, c_green, '#15803d')
    draw_block(37, 41, 26, 13, "GLOBAL MODEL", "FedAvg Consensus (global_qwen)\nShared Consolidated View", c_blue_bg, c_blue, '#1e40af')
    draw_block(68, 41, 26, 13, "AGENT 2: AML / RISK", "Qwen LoRA (qwen/agent2)\nStructuring & Compliance", c_purple_bg, c_purple, '#7e22ce')

    # Arrows to JEV Head
    draw_arrow(19, 54, 35, 63, c_green)
    draw_arrow(50, 54, 50, 63, c_blue)
    draw_arrow(81, 54, 65, 63, c_purple)

    # 3. JEV Decision Head
    draw_block(25, 63, 50, 11, "3. JEV-9B DECISION HEAD", "Linear Projection (head.safetensors) + Calibrated Probability P(True)", c_purple_bg, c_purple, '#6b21a8')

    # Arrow to Comparison
    draw_arrow(50, 74, 50, 79, c_purple)

    # 4. Comparison & Synthesis Layer
    draw_block(25, 79, 50, 11, "4. COMPARISON & SYNTHESIS LAYER", "Consensus Gate • Conflict Resolution • Key Factors", c_orange_bg, c_orange, '#c2410c')

    # Arrow to Output
    draw_arrow(50, 90, 50, 95, c_orange)

    # 5. Output / Dashboard
    draw_block(25, 95, 50, 11, "5. FINAL VERDICT & BANKING DASHBOARD", "Calibrated Score • Risk Donut • SAR Filing Protocol", c_green_bg, c_green, '#166534')

    plt.tight_layout()
    plt.savefig('architecture_blocks.png', bbox_inches='tight')
    plt.savefig('architecture_diagram.png', bbox_inches='tight')
    plt.close()
    print("architecture_blocks.png created!")

if __name__ == '__main__':
    generate_main_blocks_diagram()
