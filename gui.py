import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
import scan_functions
import mysql.connector as mysql

#List of error codes
ec = []

# Design presets for text formats

heading = QTextCharFormat()
heading.setForeground(QColor("white"))
font = QFont()        
font.setPointSize(14)
font.setFamily("Arial")
font.setBold(True)
heading.setFont(font)

sub_heading = QTextCharFormat()
sub_heading.setForeground(QColor("#e9ecef"))
font = QFont()
font.setPointSize(10)
font.setFamily("Arial")
font.setBold(False)
sub_heading.setFont(font)

blue_format = QTextCharFormat()
blue_format.setForeground(QColor("#A3E7FC"))
font = QFont()
font.setPointSize(10)
font.setFamily("Arial")
font.setBold(False)
blue_format.setFont(font)

red_format = QTextCharFormat()
red_format.setForeground(QColor("#ED254E"))
font = QFont()
font.setPointSize(10)
font.setFamily("Arial")
font.setBold(False)
red_format.setFont(font)

black_format = QTextCharFormat()
black_format.setForeground(QColor("black"))

green_format = QTextCharFormat()
green_format.setForeground(QColor("#E6F9AF"))
font = QFont()
font.setPointSize(10)
font.setFamily("Arial")
font.setBold(False)
green_format.setFont(font)

class FixerZApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FixerZ")
        self.setGeometry(100, 100, 800, 600)
        self.setAutoFillBackground(True)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        self.button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Scan", self)
        self.run_button.setStyleSheet("background-color: #18314F; color: white; font-weight: bold;")
        self.run_button.clicked.connect(self.run_scan)
        self.button_layout.addWidget(self.run_button)

        self.solutions_button = QPushButton("Possible Solutions", self)
        self.solutions_button.setStyleSheet("background-color: #1f7a8c; color: white; font-weight: bold;")
        self.solutions_button.clicked.connect(self.fetch_possible_solutions)
        self.button_layout.addWidget(self.solutions_button)

        self.layout.addLayout(self.button_layout)

        self.specs_text = QTextEdit(self)
        self.specs_text.setStyleSheet("background-color: #0D0630;border: none;")
        self.specs_text.setReadOnly(True)
        self.specs_text.setMinimumSize(780, 90)
        self.specs_text.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.specs_text)

        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet("background-color: #111111; color: white;border: none;")
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumSize(780, 360)
        self.result_text.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.result_text)

        self.start()

    def fetch_possible_solutions(self):
        try:
            self.result_text.clear()
            self.specs_text.clear()
            self.start()
            # Replace with your database connection details
            db_connection = mysql.connect(
                host="127.0.0.1",
                user="root",
                password="Nikita1234@",
                database="fixers"
            )

            if len(ec) == 0:
                self.result_text.setCurrentCharFormat(green_format)
                self.result_text.insertPlainText("NO ISSUES FOUND")

            else:
                cursor = db_connection.cursor()
                for i in ec:
                    cursor.execute("SELECT Error_Code, Possible_Solutions FROM systemissues where Error_Code = %s", (i))
                    solutions = cursor.fetchall()
                    self.result_text.insertPlainText("Possible Solutions:\n")
                    for solution in solutions:
                        self.result_text.setCurrentCharFormat(green_format)
                        self.result_text.insertPlainText(f"Error Code {solution[0]}: ")
                        self.result_text.insertPlainText(f"{solution[1]}\n")
                cursor.close()
                db_connection.close()

        except Exception as e:
            self.result_text.clear()
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText(f"Error fetching solutions: {str(e)}")

    def start(self):  
        # get system specs
        hostname_result = scan_functions.check_hostname()
        users_result = scan_functions.check_users()
        # uptime_result = scan_functions.check_system_uptime()
        boot_result = scan_functions.calculate_boot_time_duration()
        arch_result = scan_functions.check_system_architecture()
        load_result = scan_functions.check_system_load()
        version_result = scan_functions.check_system_version()

        # display system specs
        self.specs_text.setCurrentCharFormat(heading)
        self.specs_text.insertPlainText("Basic System Details Results:\n")
        self.specs_text.setCurrentCharFormat(sub_heading)
        self.specs_text.insertPlainText("Hostname:\t\t\t" + hostname_result + "\n")
        self.specs_text.insertPlainText("Logged In Users:\t\t" + users_result + "\n")
        # self.specs_text.insertPlainText("System Uptime:" + uptime_result + "\n")
        self.specs_text.insertPlainText("Time since last boot:\t\t" + boot_result + "\n")
        self.specs_text.insertPlainText("System Architecture:\t\t" + arch_result + "\n")
        self.specs_text.insertPlainText("System Version:\t\t" + version_result + "\n")
        self.specs_text.insertPlainText("System Load:\t\t" + load_result + "\n")

    def run_scan(self):
        ec = []
        self.result_text.clear()
        self.specs_text.clear()
        self.start()
        cpu_result = scan_functions.check_cpu_usage()
        ram_result = scan_functions.check_ram_usage()
        disk_result = scan_functions.check_disk_usage()
        network_result = scan_functions.check_network_status()
        battery_result = scan_functions.check_battery_status()
        usb_status = scan_functions.check_usb_ports()

        issue = 0

        self.result_text.setCurrentCharFormat(heading)
        self.result_text.insertPlainText("Troubleshooting Results:\n")
        self.result_text.setCurrentCharFormat(sub_heading)
        # CPU TEST RESULT 
        if "High" in cpu_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n")
            issue += 1
            ec.append(["HI4"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n")
            

        # RAM TEST RESULT
        if "High" in ram_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n")
            issue += 1
            ec.append(["HI5"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n")
        
        # NETWORK TEST RESULT
        if "error" in network_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n")
            issue += 1
            ec.append(["SI1"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n")

        # BATTERY TEST RESULT
        if "not" in battery_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Battery Status: \t" + battery_result + "\n")
            issue += 1
            ec.append(["HI3"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Battery Status: \t" + battery_result + "\n")
        
        #USB TEST RESULT
        if "not" in usb_status or "Error" in usb_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("USB Status: \t" + usb_status + "\n")
            issue += 1
            ec.append(["HI2"])
        elif "No USB devices found." in usb_status:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("USB Status: \t" +"USB device not found.\n")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("USB Status: \t" + usb_status + "\n")

        # DISK TEST RESULT
        if "High" in disk_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Disk Status: \n" + disk_result + "\n")
            issue += 1
            ec.append(["HI6"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Disk Status: " + disk_result + "\n")

        #FINAL RESULT
        if issue != 0:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("\n\nPotential issues detected. \nClick on the Possible Solutions button\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #0D0630; }")
    window = FixerZApp()
    window.show()
    sys.exit(app.exec_())
