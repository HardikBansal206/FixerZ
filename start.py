import tkinter as tk
from tkinter import ttk
import os
import psutil
import subprocess

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

def run_scan():
    # Clear previous results
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    
    cpu_result = check_cpu_usage()
    ram_result = check_ram_usage()
    disk_result = check_disk_usage()

    # Display the results
    result_text.insert(tk.END, "Troubleshooting Results:\n", "blue")
    result_text.insert(tk.END, "CPU Status: " + cpu_result + "\n", "blue")
    result_text.insert(tk.END, "RAM Status: " + ram_result + "\n", "blue")
    result_text.insert(tk.END, "Disk Status: " + disk_result + "\n", "blue")

    if "High" in cpu_result or "High" in ram_result or "High" in disk_result:
        result_text.insert(tk.END, "Potential issues detected. Consider further investigation.\n", "red")
    else:
        result_text.insert(tk.END, "All components are working fine.\n", "blue")
    
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("FixerZ")

# Create a frame for the controls
control_frame = ttk.Frame(root)
control_frame.pack(padx=10, pady=10)

# Create a "Run Scan" button
run_button = ttk.Button(control_frame, text="Run Scan", command=run_scan)
run_button.grid(row=0, column=0, padx=5, pady=5)

# Create a text widget to display results
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=50)
result_text.pack(padx=10, pady=10)
result_text.tag_config("red", foreground="red")
result_text.tag_config("blue", foreground="blue")
result_text.config(state=tk.DISABLED)

root.mainloop()
