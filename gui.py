import tkinter as tk
from tkinter import ttk
import subprocess
import scan_functions
import mysql.connector

def run_scan():
    # Clear previous results
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    
    cpu_result = scan_functions.check_cpu_usage()
    ram_result = scan_functions.check_ram_usage()
    disk_result = scan_functions.check_disk_usage()
    network_result = scan_functions.check_network_status()
    battery_result = scan_functions.check_battery_status()
    available_disk_space_result = scan_functions.check_available_disk_space()  # New scan function
    hostname_result = scan_functions.check_hostname()  # New scan function
    users_result = scan_functions.check_users()  # New scan function
    uptime_result = scan_functions.check_system_uptime()  # New scan function
    arch_result = scan_functions.check_system_architecture()  # New scan function
    load_result = scan_functions.check_system_load()  # New scan function
    version_result = scan_functions.check_system_version()  # New scan function

    # Display the results
    result_text.insert(tk.END, "Troubleshooting Results:\n", "blue")
    result_text.insert(tk.END, "CPU Status: " + cpu_result + "\n", "blue")
    result_text.insert(tk.END, "RAM Status: " + ram_result + "\n", "blue")
    result_text.insert(tk.END, "Disk Status: " + disk_result + "\n", "blue")
    result_text.insert(tk.END, "Network Status: " + network_result + "\n", "blue")
    result_text.insert(tk.END, "Battery Status: " + battery_result + "\n", "blue")
    result_text.insert(tk.END, "Available Disk Space:" + available_disk_space_result + "\n", "blue")
    result_text.insert(tk.END, "Hostname:" + hostname_result + "\n", "blue")
    result_text.insert(tk.END, "Logged In Users:" + users_result + "\n", "blue")
    result_text.insert(tk.END, "System Uptime:" + uptime_result + "\n", "blue")
    result_text.insert(tk.END, "System Architecture:" + arch_result + "\n", "blue")
    result_text.insert(tk.END, "System Load:" + load_result + "\n", "blue")
    result_text.insert(tk.END, "System Version:" + version_result + "\n", "blue")

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

# Style
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("TText", font=("Helvetica", 12))

# Create a "Run Scan" button
run_button = ttk.Button(control_frame, text="Run Scan", command=run_scan, style="TButton")
run_button.grid(row=0, column=0, padx=5, pady=5)

# Create a text widget to display results
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=50)
result_text.pack(padx=10, pady=10)
result_text.tag_config("red", foreground="red")
result_text.tag_config("blue", foreground="blue")
result_text.config(state=tk.DISABLED)

root.mainloop()
