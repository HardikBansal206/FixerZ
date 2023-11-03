import os
import psutil
import platform
from datetime import datetime
import subprocess
import wmi
import cv2
import pyaudio
import cpuinfo
from screeninfo import get_monitors
import GPUtil


def check_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent < 80:
        return f"CPU Usage is normal: {cpu_percent}%"
    else:
        return f"High CPU usage detected: {cpu_percent}%"

def check_ram_usage():
    ram = psutil.virtual_memory()
    if ram.percent < 80:
        return f"RAM usage is normal: {ram.percent}%"
    else:
        return f"High RAM usage detected: {ram.percent}%"

def check_disk_usage():
    partitions = psutil.disk_partitions()
    high_usage_disks = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        if usage.percent >= 80:
            high_usage_disks.append(f"High disk usage on {partition.device}: {usage.percent}%")
    if high_usage_disks:
        return high_usage_disks
    else:
        return ["Disk usage is normal."]

def check_network_status():
    try:
        a = psutil.net_if_stats()
        if "Wi-Fi" not in a:
            return "Network error:"
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

def calculate_boot_time_duration():
    try:
        boot_time_seconds = psutil.boot_time()
        current_time_seconds = datetime.now().timestamp()
        boot_duration_seconds = current_time_seconds - boot_time_seconds
        boot_duration_formatted = format_boot_time_duration(boot_duration_seconds)
        return boot_duration_formatted
    except Exception as e:
        return f"Boot time duration retrieval error: {str(e)}"

def format_boot_time_duration(duration_seconds):
    minutes, seconds = divmod(duration_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"


def check_system_architecture():
    try:
        arch = platform.architecture()
        return f"{arch[0]}"
    except Exception as e:
        return f"Architecture retrieval error: {str(e)}"
    
def check_system_load():
    try:
        # Run the wmic command to get load information
        result = subprocess.check_output(["wmic", "cpu", "get", "loadpercentage"])
        # Decode the result and remove any unwanted characters
        load_percentage = result.decode("utf-8").strip().split("\n")[1]
        return f"Load Percentage: {load_percentage}%"
    except Exception as e:
        return f"Load percentage retrieval error: {str(e)}"
    
def check_system_version():
    try:
        version = platform.version()
        return f"{version}"
    except Exception as e:
        return f"Version retrieval error: {str(e)}"

def check_usb_ports():
    usb_device_info = []
    c = wmi.WMI()

    for device in c.Win32_PnPEntity():
        caption = device.Caption
        if caption and 'USB' in caption:
            usb_device_info.append(caption)

    return usb_device_info


def check_camera():
    try:
        cap = cv2.VideoCapture(0)  # Open the default camera (usually the built-in webcam)
        if cap.isOpened():
            return "Camera is working fine."
        else:
            return "Camera is not working."
    except Exception as e:
        return f"Camera error: {str(e)}"

def check_microphone():
    try:
        audio = pyaudio.PyAudio()
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if "microphone" in device_info["name"].lower():
                return "Microphone is working fine."
        return "Microphone is not working."
    except Exception as e:
        return f"Microphone error: {str(e)}"

def get_cpu_info():
    cpu_info = cpuinfo.get_cpu_info()
    processor_name = cpu_info['brand_raw']
    return processor_name 

def get_gpu_info():
    gpu_info = GPUtil.getGPUs()
    if gpu_info:
        gpu = gpu_info[0]  # Assuming you have at least one GPU
        gpu_model = gpu.name
        gpu_memory_total = gpu.memoryTotal
        gpu_memory_used = gpu.memoryUsed
        gpu_utilization = round(((gpu_memory_used) / gpu_memory_total )* 100, 2) # In percentage

        return str(gpu_model) + " \n(" + str(gpu_utilization) + "% used)"
    else:
        print("Not available")

def get_ram_info():
    ram_info = psutil.virtual_memory()
    total_ram_gb = round(ram_info.total / (1024 ** 3), 2)
    return str(round(total_ram_gb, 2)) + " GB \n(" + str(round(ram_info.percent,2)) + "% used)"

def get_display_info():
    # Get the primary display's size (resolution)
    primary_display = get_monitors()[0]  # Assuming the first monitor is the primary one
    resolution = (primary_display.width, primary_display.height)
    return str(resolution[0]) + " x " + str(resolution[1]) 

def get_storage_info():
    # Get information for all available drives
    drive_info = psutil.disk_partitions(all=True)

    total_available_storage_gb = 0
    total_storage_gb = 0

    for drive in drive_info:
        drive_letter = drive.device
        storage_info = psutil.disk_usage(drive.mountpoint)
        
        total_storage_gb += storage_info.total / (1024 ** 3)  # Total storage capacity in GB
        available_storage_gb = storage_info.free / (1024 ** 3)  # Available storage space in GB
        
        total_available_storage_gb += available_storage_gb
    return str(round(total_storage_gb, 2)) + " GB \n(" + str(round(total_available_storage_gb, 2)) + " GB available)"

a = psutil.net_if_stats()
print(a)
if "Wi-Fi" in a:
    print("Helo")
else:
    print("Bye")