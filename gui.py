import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
import scan_functions
import mysql.connector

class FixerZApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FixerZ")
        self.setGeometry(100, 100, 800, 600)
        self.setAutoFillBackground(True)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.run_button = QPushButton("Run Scan", self)
        self.run_button.setStyleSheet("background-color: #1a6985; color: white; font-weight: bold;")
        self.run_button.clicked.connect(self.run_scan)
        self.layout.addWidget(self.run_button)

        self.solutions_button = QPushButton("Possible Solutions", self)
        self.solutions_button.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        self.solutions_button.clicked.connect(self.fetch_possible_solutions)
        self.layout.addWidget(self.solutions_button)

        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet("background-color: #111111; color: white;border: none;")
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

    def fetch_possible_solutions(self):
        try:
            # Define different formats for colors
            blue_format = QTextCharFormat()
            blue_format.setForeground(QColor("#1a6985"))
            red_format = QTextCharFormat()
            red_format.setForeground(QColor("red"))
            # Replace with your database connection details
            db_connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Nikita1234@",
                database="fixers"
            )

            cursor = db_connection.cursor()
            cursor.execute("SELECT Error_Code, Possible_Solutions FROM systemissues")
            solutions = cursor.fetchall()

            # Clear existing text
            self.result_text.clear()

            # Define different formats for colors
            blue_format = QTextCharFormat()
            blue_format.setForeground(QColor("blue"))

            # Display solutions in the text widget
            self.result_text.insertPlainText("Possible Solutions:\n")
            for solution in solutions:
                self.result_text.setCurrentCharFormat(blue_format)
                self.result_text.insertPlainText(f"Error Code {solution[0]}: ")
                self.result_text.insertPlainText(f"{solution[1]}\n")

            cursor.close()
            db_connection.close()
        except Exception as e:
            self.result_text.clear()
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText(f"Error fetching solutions: {str(e)}")

    def run_scan(self):
        self.result_text.clear()

        # Define different formats for colors
        
        heading = QTextCharFormat()
        heading.setForeground(QColor("white"))
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Arial")
        font.setBold(True)
        heading.setFont(font)

        sub_heading = QTextCharFormat()
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Arial")
        font.setBold(False)
        sub_heading.setFont(font)

        blue_format = QTextCharFormat()
        blue_format.setForeground(QColor("#3772FF"))
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Arial")
        font.setBold(False)
        blue_format.setFont(font)

        red_format = QTextCharFormat()
        red_format.setForeground(QColor("#DF2935"))
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Arial")
        font.setBold(False)
        red_format.setFont(font)

        black_format = QTextCharFormat()
        black_format.setForeground(QColor("black"))

        cpu_result = scan_functions.check_cpu_usage()
        ram_result = scan_functions.check_ram_usage()
        disk_result = scan_functions.check_disk_usage()
        network_result = scan_functions.check_network_status()
        battery_result = scan_functions.check_battery_status()
        hostname_result = scan_functions.check_hostname()
        users_result = scan_functions.check_users()
        # uptime_result = scan_functions.check_system_uptime()
        boot_result = scan_functions.calculate_boot_time_duration()
        arch_result = scan_functions.check_system_architecture()
        load_result = scan_functions.check_system_load()
        version_result = scan_functions.check_system_version()

        issue = 0
        self.result_text.setCurrentCharFormat(heading)
        self.result_text.insertPlainText("Basic System Details Results:\n")
        
        self.result_text.setCurrentCharFormat(sub_heading)
        self.result_text.insertPlainText("Hostname:\t\t\t" + hostname_result + "\n")
        self.result_text.insertPlainText("Logged In Users:\t\t" + users_result + "\n")
        # self.result_text.insertPlainText("System Uptime:" + uptime_result + "\n")
        self.result_text.insertPlainText("Time since last boot:\t\t" + boot_result + "\n")
        self.result_text.insertPlainText("System Architecture:\t\t" + arch_result + "\n")
        self.result_text.insertPlainText("System Load:\t\t" + load_result + "\n")
        self.result_text.insertPlainText("System Version:\t\t" + version_result + "\n")

        self.result_text.setCurrentCharFormat(heading)
        self.result_text.insertPlainText("\n\nTroubleshooting Results:\n")
        self.result_text.setCurrentCharFormat(sub_heading)
        # CPU TEST RESULT 
        if "High" in cpu_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n")
            issue += 1
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n")

        # RAM TEST RESULT
        if "High" in ram_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n")
            issue += 1
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n")
        
        # NETWORK TEST RESULT
        if "error" in network_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n")
            issue += 1
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n")

        # BATTERY TEST RESULT
        if "not" in battery_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Battery Status: \t" + battery_result + "\n")
            issue += 1
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Battery Status: \t" + battery_result + "\n")
        
        # DISK TEST RESULT
        if "High" in disk_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Disk Status: \n" + disk_result + "\n")
            issue += 1
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Disk Status: " + disk_result + "\n")
        
        #FINAL RESULT
        if issue != 0:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("\n\nPotential issues detected. \nClick on the Possible Solutions button\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #2c3e50; }")
    window = FixerZApp()
    window.show()
    sys.exit(app.exec_())
