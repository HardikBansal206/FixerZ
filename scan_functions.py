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
