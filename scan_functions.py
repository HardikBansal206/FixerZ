import os
import psutil

def check_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent < 80:
        return "CPU usage is normal."
    else:
        return f"High CPU usage detected: {cpu_percent}%"

def check_ram_usage():
    ram = psutil.virtual_memory()
    if ram.percent < 80:
        return "RAM usage is normal."
    else:
        return f"High RAM usage detected: {ram.percent}%"

def check_disk_usage():
    partitions = psutil.disk_partitions()
    disk_status = ""
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent >= 80:
            disk_status += f"High disk usage on {partition.device}: {usage.percent}%\n"
    if disk_status:
        return disk_status
    else:
        return "Disk usage is normal."

def check_network_status():
    try:
        psutil.net_if_stats()
        return "Network is operational."
    except Exception as e:
        return f"Network error: {str(e)}"

def check_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        if battery.power_plugged:
            return f"Battery is charging ({battery.percent}% charged)."
        else:
            return f"Battery is discharging ({battery.percent}% charged)."
    else:
        return "Battery status not available."

def check_temperature():
    try:
        temperatures = psutil.sensors_temperatures()
        if "coretemp" in temperatures:
            core_temp = temperatures["coretemp"]
            if core_temp:
                return f"CPU Core Temperature: {core_temp[0].current}°C"
    except Exception as e:
        return f"Temperature reading error: {str(e)}"
