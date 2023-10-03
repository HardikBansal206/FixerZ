import os
import psutil
import platform
from datetime import datetime

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

def check_available_disk_space():
    partitions = psutil.disk_partitions()
    disk_status = ""
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent < 80:
            disk_status += f"Disk space on {partition.device} is normal.\n"
        else:
            disk_status += f"Low disk space on {partition.device}: {usage.percent}%\n"
    return disk_status

def check_hostname():
    hostname = platform.node()
    return f"{hostname}"

def check_users():
    try:
        users = os.getlogin()
        return f"{users}"
    except Exception as e:
        return f"User retrieval error: {str(e)}"

def check_system_uptime():
    try:
        uptime_seconds = psutil.boot_time()
        uptime_datetime = datetime.fromtimestamp(uptime_seconds)
        formatted_uptime = uptime_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_uptime
    except Exception as e:
        return f"Uptime retrieval error: {str(e)}"
    
def check_system_architecture():
    try:
        arch = platform.architecture()
        return f"{arch[0]}"
    except Exception as e:
        return f"Architecture retrieval error: {str(e)}"
    
def check_system_load():
    try:
        load = psutil.getloadavg()
        return f"Load average (1min, 5min, 15min): {load[0]}, {load[1]}, {load[2]}"
    except Exception as e:
        return f"Load average retrieval error: {str(e)}"
    
def check_system_version():
    try:
        version = platform.version()
        return f"{version}"
    except Exception as e:
        return f"Version retrieval error: {str(e)}"
    

