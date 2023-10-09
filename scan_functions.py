import os
import psutil
import platform
from datetime import datetime
import subprocess
import wmi
import cv2
import pyaudio


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

# def check_input_devices():
#     try:
#         # Check mouse movement with a timeout
#         max_retries = 5  # Adjust the number of retries as needed
#         for _ in range(max_retries):
#             try:
#                 pyautogui.move(10, 10, duration=0.5)
#                 pyautogui.move(-10, -10, duration=0.5)
#                 break  # Exit the loop if successful
#             except Exception as e:
#                 time.sleep(1)  # Wait for a moment before retrying

#         # Check keyboard input
#         pyautogui.write("Test Keyboard Input", interval=0.1)

#         return "Mouse and keyboard are working fine."
#     except Exception as e:
#         return f"Error checking input devices: {e}"
