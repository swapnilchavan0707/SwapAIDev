import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
from utils.theme_config import apply_global_theme, FONT_STYLE

# Output Directory
REPORT_DIR = "forensic_reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def save_urgency_meter(score, filename):
    """Generates and saves the Urgency Gauge as a PNG."""
    apply_global_theme()
    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})

    val = (score / 100) * np.pi
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)

    # Background segments
    ax.bar(x=[0, np.pi / 3, 2 * np.pi / 3], width=np.pi / 3, height=0.5, bottom=2,
           color=['#238636', '#e3b341', '#f85149'], alpha=0.3, align='edge')

    # Needle
    ax.annotate("", xy=(val, 2.5), xytext=(0, 0),
                arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="white"))

    ax.set_axis_off()
    plt.title(f"Threat Score: {score:.0f}%", fontsize=16, fontname=FONT_STYLE, pad=20)

    path = os.path.join(REPORT_DIR, f"{filename}_urgency.png")
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    return path


def save_link_map(email_data, filename):
    """Generates and saves the Infrastructure Map as a PNG."""
    apply_global_theme()
    G = nx.DiGraph()

    sender = email_data['sender']
    email_node = "Payload"
    G.add_edge(sender, email_node)

    for link in email_data['links']:
        G.add_edge(email_node, link['domain'])

    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(10, 7))

    # Neon Colors (Cyber-Blue & Pink)
    colors = ['#f72585' if n == sender else '#4cc9f0' for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=2500, font_size=9, font_family=FONT_STYLE,
            edge_color='#30363d', arrows=True, ax=ax)

    plt.title("Infrastructure Topology Map", fontsize=18, fontname=FONT_STYLE)

    path = os.path.join(REPORT_DIR, f"{filename}_map.png")
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)
    return path