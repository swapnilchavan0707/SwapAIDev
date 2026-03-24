import psutil
import shutil


def get_pc_health_metrics():
    # 1. CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # 2. RAM Usage
    memory = psutil.virtual_memory()
    ram_data = {'Total': memory.total, 'Used': memory.used, 'Free': memory.available, 'Percent': memory.percent}

    # 3. Disk Usage (Main Drive)
    disk = shutil.disk_usage("/")
    disk_data = {'Total': disk.total, 'Used': disk.used, 'Free': disk.free, 'Percent': (disk.used / disk.total) * 100}

    return {
        'cpu': cpu_usage,
        'ram': ram_data,
        'disk': disk_data
    }
