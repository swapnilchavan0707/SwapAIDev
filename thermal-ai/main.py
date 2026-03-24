import os
import sys
from src.heat_engine import get_system_temps
from src.visualizer import save_thermal_heatmap, save_temp_bar_chart

def main():
    # 1. Setup project paths
    output_folder = 'data/thermal_reports'
    os.makedirs(output_folder, exist_ok=True)

    print("========================================")
    print("   Thermal Report Analysis     ")
    print("========================================\n")

    # 2. Inform the user about Simulation Mode
    # Since standard Windows users can't access hardware sensors directly,
    # we use simulated data to ensure the AI visualization logic works.
    print("![Notice]: Running in AI Simulation Mode.")
    print("Generating figures based on predicted hardware thermal zones...\n")

    # 3. Get Thermal Data (Forcing simulation for compatibility)
    # This calls the get_system_temps function you updated in heat_engine.py
    df, status = get_system_temps()

    if "Success" in status and df is not None:
        print(f"Analyzing {len(df)} simulated thermal zones.\n")

        # 4. Generate Heatmap Figure
        heatmap_path = os.path.join(output_folder, 'thermal_heatmap.png')
        save_thermal_heatmap(df, heatmap_path)
        print(f"[1/2] Heatmap figure saved: {heatmap_path}")

        # 5. Generate Bar Chart Figure
        chart_path = os.path.join(output_folder, 'temp_analysis_chart.png')
        save_temp_bar_chart(df, chart_path)
        print(f"[2/2] Analysis graph saved: {chart_path}")

        print("\n--- Project Execution Complete ---")
        print(f"All outputs are available in: {os.path.abspath(output_folder)}")
    else:
        print(f"Failed: {status}")

if __name__ == "__main__":
    main()