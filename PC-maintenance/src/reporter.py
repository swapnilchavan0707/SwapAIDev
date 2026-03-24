import matplotlib.pyplot as plt


def save_maintenance_report(metrics, output_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # 1. Disk Usage Pie Chart
    disk_labels = ['Used Space', 'Free Space']
    disk_sizes = [metrics['disk']['Used'], metrics['disk']['Free']]
    ax1.pie(disk_sizes, labels=disk_labels, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'], startangle=140)
    ax1.set_title(f"Disk Health (Total: {metrics['disk']['Total'] // (2 ** 30)} GB)")

    # 2. RAM Usage Gauge (Horizontal Bar)
    ax2.barh(['RAM Usage'], [metrics['ram']['Percent']], color='green' if metrics['ram']['Percent'] < 80 else 'red')
    ax2.set_xlim(0, 100)
    ax2.set_title(f"RAM Load: {metrics['ram']['Percent']}%")
    ax2.grid(axis='x', linestyle='--', alpha=0.7)

    plt.suptitle(f"PC Maintenance Health Report\nCPU Load: {metrics['cpu']}%", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_path)
    plt.close()
