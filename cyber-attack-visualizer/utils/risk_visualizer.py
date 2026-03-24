import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.theme_config import apply_global_theme, FONT_STYLE


def generate_urgency_meter(score):
    """
    Creates a Gauge-style 'Urgency Meter' using a Matplotlib polar plot.
    score: 0 to 100
    """
    # Apply the global font and dark theme
    apply_global_theme()

    fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={'projection': 'polar'})

    # Gauge math: Convert 0-100 score to 0-PI radians
    val = (score / 100) * np.pi
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)

    # Background Gauge Segments (Green, Yellow, Red)
    ax.bar(x=[0, np.pi / 3, 2 * np.pi / 3], width=np.pi / 3, height=0.5, bottom=2,
           color=['#28a745', '#ffc107', '#dc3545'], alpha=0.3, align='edge')

    # The Needle
    ax.annotate("", xy=(val, 2.5), xytext=(0, 0),
                arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="white", shrinkA=0))

    # Text Labels
    ax.set_axis_off()
    plt.title(f"Threat Urgency: {score:.0f}%", fontsize=16, pad=20, fontname=FONT_STYLE)

    # Label the safe/critical zones
    ax.text(0, 2.8, "LOW", ha='center', va='center', fontname=FONT_STYLE, color="gray")
    ax.text(np.pi, 2.8, "HIGH", ha='center', va='center', fontname=FONT_STYLE, color="gray")

    return fig


def generate_reputation_plot(sender_data_list):
    """
    Creates a Bubble Chart for Sender Reputation.
    """
    apply_global_theme()

    if not sender_data_list:
        return None

    df = pd.DataFrame(sender_data_list)

    fig, ax = plt.subplots(figsize=(8, 5))

    scatter = ax.scatter(
        x=df['risk_score'],
        y=df['tld'],
        s=df['frequency'] * 500,
        c=df['risk_score'],
        cmap='YlOrRd',
        alpha=0.7,
        edgecolors="white"
    )

    ax.set_xlabel("Domain Risk Score", fontname=FONT_STYLE)
    ax.set_ylabel("TLD Extension", fontname=FONT_STYLE)
    plt.title("Sender Reputation Analysis", fontsize=16, fontname=FONT_STYLE)

    return fig