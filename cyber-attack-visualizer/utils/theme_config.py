import matplotlib.pyplot as plt
import plotly.io as pio

# Global Font Configuration
FONT_STYLE = "Times New Roman"


def apply_global_theme():
    """
    Applies Times New Roman and Dark Theme to all Matplotlib
    and Plotly visualizations in the project.
    """
    # Matplotlib Global Settings
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = [FONT_STYLE]
    plt.style.use('dark_background')

    # Plotly Global Settings
    pio.templates.default = "plotly_dark"