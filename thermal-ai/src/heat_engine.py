import pandas as pd
import numpy as np
import platform
import random


def get_system_temps(simulate=True):
    """
    Fetches real temps if possible; otherwise, generates
    realistic simulated data for the AI project.
    """
    if not simulate:
        # (Keep your existing WMI/psutil logic here for real attempts)
        pass

        # --- SIMULATION LOGIC ---
    # We create a list of common laptop 'Thermal Zones'
    sensors = ['CPU Core 1', 'CPU Core 2', 'GPU Die', 'Battery', 'Motherboard']
    data = []

    for sensor in sensors:
        # Generate realistic random temps between 45C and 85C
        current_temp = round(random.uniform(45.0, 82.0), 1)
        data.append({
            'Sensor': sensor,
            'Current': current_temp,
            'Critical': 100.0
        })

    return pd.DataFrame(data), "Success (Simulated)"