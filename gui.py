import tkinter as tk
from tkinter import ttk
import subprocess
import scan_functions

def run_scan():
    # Clear previous results
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    
    cpu_result = scan_functions.check_cpu_usage()
    ram_result = scan_functions.check_ram_usage()
    disk_result = scan_functions.check_disk_usage()

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
