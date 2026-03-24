import matplotlib.pyplot as plt
import seaborn as sns


def save_thermal_heatmap(df, output_path):
    """
    Generates a Heatmap figure showing thermal intensity.
    """
    plt.figure(figsize=(8, len(df) * 0.6 + 2))
    # Prepare data for heatmap
    heatmap_data = df.set_index('Sensor')[['Current']]

    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='YlOrRd',
                cbar_kws={'label': 'Temp °C'}, annot_kws={"size": 12})

    plt.title('Internal Hardware Heatmap', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_temp_bar_chart(df, output_path):
    """
    Generates a Bar Chart comparing Current Temps to Safety Limits.
    """
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    # Plot Current Temps
    bars = plt.bar(df['Sensor'], df['Current'], color='salmon', label='Current Temp')

    # Add labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval}°C', ha='center', va='bottom')

    plt.axhline(y=80, color='red', linestyle='--', label='Warning Threshold (80°C)')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Temperature (°C)')
    plt.title('Hardware Temperature Analysis', fontsize=14)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
