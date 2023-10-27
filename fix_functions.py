import subprocess
import string 
import os

# Disk Cleanup
def disk_cleanup_setup(profile_number):
    configure_command = f'cleanmgr /sageset:{profile_number}'
    try:
        subprocess.run(configure_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "success"
    except Exception as e:
        return(f"An error occurred during setup: {e}")

def disk_cleanup(profile_number):
    cleanup_command = f'cleanmgr /sagerun:{profile_number}'
    try:
        result = subprocess.run(cleanup_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return(result.stdout)
        else:
            return(result.stderr)
    except Exception as e:
        return(f"An error occurred during cleanup: {e}")


# Windows Defender
def run_windows_defender_quick_scan():
    command = '"%ProgramFiles%\\Windows Defender\\MpCmdRun.exe" -Scan -ScanType 1'
    try:
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run("start ms-settings:windowsdefender", shell=True)
    except Exception as e:
        return(f"An error occurred during the scan: {e}")

def run_windows_defender_full_scan():
    command = '"%ProgramFiles%\\Windows Defender\\MpCmdRun.exe" -Scan -ScanType 2'
    try:
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run("start ms-settings:windowsdefender", shell=True)
    except Exception as e:
        return(f"An error occurred during the scan: {e}")


# Disk Fragmentation
def analyze_disk_drive(drive_letter):
    command = f'defrag {drive_letter}: /A'
    try:
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return(f"Disk analysis initiated for drive {drive_letter}.")
    except Exception as e:
        return(f"An error occurred during the analysis of drive {drive_letter}: {e}")

def defragment_disk_drive(drive_letter):
    command = f'defrag {drive_letter}: /O'
    try:
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return(f"Disk defragmentation initiated for drive {drive_letter}.")
    except Exception as e:
        return(f"An error occurred during the defragmentation of drive {drive_letter}: {e}")

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        if os.path.exists(letter + ":\\"):
            drives.append(letter)
    return drives

def analyze_all_drives():
    drives = get_available_drives()
    err = 0
    for drive in drives:
        res = analyze_disk_drive(drive)
        if "error" in res.lower():
            err += 1
    if err == 0:
        return "success"
    else:
        return "failure"

def defragment_all_drives():
    drives = get_available_drives()
    err = 0
    for drive in drives:
        res = defragment_disk_drive(drive)
        if "error" in res.lower():
            err += 1
    if err == 0:
        return "success"
    else:
        return "failure"
    
# run_windows_defender_full_scan()
# run_windows_defender_quick_scan()
