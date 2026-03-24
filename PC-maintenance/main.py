import os
from src.health_monitor import get_pc_health_metrics
from src.reporter import save_maintenance_report


def main():
    output_dir = 'data/maintenance_reports'
    os.makedirs(output_dir, exist_ok=True)

    print("--- Starting PC Maintenance Scan ---")
    stats = get_pc_health_metrics()

    report_path = os.path.join(output_dir, 'pc_health_summary.png')
    save_maintenance_report(stats, report_path)

    print(f"Success! Maintenance report generated at: {report_path}")
    if stats['disk']['Percent'] > 90:
        print("ALERT: Disk is almost full! Recommend cleaning temp files.")


if __name__ == "__main__":
    main()
