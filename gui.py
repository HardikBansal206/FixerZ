import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QProgressBar, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont 
from PyQt5.QtCore import Qt, QPropertyAnimation
import scan_functions
import mysql.connector as mysql
from docx import Document
import webbrowser

#List of error codes
global ec
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
green_format.setForeground(QColor("#3CB043"))
font = QFont()
font.setPointSize(10)
font.setFamily("Arial")
font.setBold(False)
green_format.setFont(font)

class FixerZApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FixerZ")
        self.setGeometry(100, 100, 800, 830)
        self.setAutoFillBackground(True)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        
        self.button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Scan", self)
        self.run_button.setStyleSheet("background-color: #65B891; color: white; font-weight: bold; border-radius: 5px; border: none; min-width: 200px; max-width: 400px;min-height: 40px; max-height: 60px;")
        self.run_button.clicked.connect(self.run_scan)
        self.button_layout.addWidget(self.run_button)

        self.solutions_button = QPushButton("Possible Solutions", self)
        self.solutions_button.setStyleSheet("background-color: #1f7a8c; color: white; font-weight: bold; border-radius: 5px; border: none; min-width: 200px; max-width: 400px;min-height: 40px; max-height: 60px;")
        self.solutions_button.clicked.connect(self.fetch_possible_solutions)
        self.button_layout.addWidget(self.solutions_button)
        self.solutions_button.hide()

        self.layout.addLayout(self.button_layout)

        self.specs_text = QTextEdit(self)
        self.specs_text.setStyleSheet("background-color: #0D0630;border: none;")
        self.specs_text.setReadOnly(True)
        self.specs_text.setContentsMargins(10, 10, 10, 10)
        self.specs_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.specs_text)

        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet("background-color: #111111; color: white;border: none;")
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumSize(780, 525)
        self.result_text.setContentsMargins(10, 10, 10, 10)
        self.layout.addWidget(self.result_text)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.layout.addWidget(self.progress_bar)

        self.export_layout = QHBoxLayout()
        self.export = QPushButton("Export", self)
        self.export.setStyleSheet("background-color: #0000FF; color: white; font-weight: bold; border-radius: 5px; border: none; min-width: 200px; max-width: 400px;min-height: 40px; max-height: 60px;")
        self.export.clicked.connect(self.export_to_word_file_run)
        self.export_layout.addWidget(self.export)
        self.layout.addLayout(self.export_layout)
        self.export.hide()

        self.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(int(value))
        QApplication.processEvents()  

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
                    cursor.execute("SELECT Error_Detail, Possible_Solutions FROM systemissues where Error_Code = %s", (i))
                    solutions = cursor.fetchall()
                    for solution in solutions:
                        self.result_text.setCurrentCharFormat(green_format)
                        self.result_text.insertPlainText(f"{solution[0]}: ")
                        self.result_text.insertPlainText("Possible Solutions:")
                        self.result_text.insertPlainText(f"{solution[1]}\n")
                        view_more_button = QPushButton("View More", self)
                    view_more_button.setStyleSheet("color: blue; text-decoration: underline;")
                    view_more_button.clicked.connect(lambda checked, desc=solution[0]: self.view_more_clicked(desc))
                    self.layout.addWidget(view_more_button)
                self.result_text.insertPlainText("\n")
            cursor.close()
            db_connection.close()

        except Exception as e:
            self.result_text.clear()
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText(f"Error fetching solutions: {str(e)}")

    def view_more_clicked(self, error_description):
        self.search_error_solution(error_description)
        QMessageBox.information(self, "View More Clicked", "You clicked the 'View More' button.")

    def start(self):  
        # get system specs
        hostname_result = scan_functions.check_hostname()
        users_result = scan_functions.check_users()
        # uptime_result = scan_functions.check_system_uptime()
        boot_result = scan_functions.calculate_boot_time_duration()
        arch_result = scan_functions.check_system_architecture()
        load_result = scan_functions.check_system_load()
        version_result = scan_functions.check_system_version()
        battery_result = scan_functions.check_battery_status()

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
        self.specs_text.insertPlainText("Battery Status:\t\t" + battery_result + "\n")

    def search_error_solution(error_description):
        search_query = f"Step wise solution for troubleshooting {error_description}"
        webbrowser.open_new_tab("https://www.google.com/search?q=" + search_query)

    def run_scan(self):
        ec.clear()
        self.result_text.clear()
        self.specs_text.clear()
        self.start()
        self.export.hide()

        total_tests = 7
        completed_tests = 0

        self.progress_bar.show()
        self.solutions_button.hide()
        self.result_text.setMinimumHeight(500)
        self.update_progress(0)  # Initialize the progress bar
        QApplication.processEvents()  # Force the GUI to update

        self.result_text.insertPlainText("Checking System Status...\n")

        cpu_result = scan_functions.check_cpu_usage()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)

        ram_result = scan_functions.check_ram_usage()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        disk_result = scan_functions.check_disk_usage()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        network_result = scan_functions.check_network_status()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        usb_status = scan_functions.check_usb_ports()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        camera_status = scan_functions.check_camera()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        mic_status = scan_functions.check_microphone()
        completed_tests += 1
        self.update_progress(completed_tests / total_tests * 100)
        
        self.progress_bar.hide()
        self.result_text.setMinimumHeight(525)

        # mouse_keyboard_status = scan_functions.check_input_devices()

        issue = 0

        self.result_text.clear()
        self.result_text.setCurrentCharFormat(heading)
        self.result_text.insertPlainText("Troubleshooting Results:\n")
        self.result_text.setCurrentCharFormat(sub_heading)
        # CPU TEST RESULT 
        if "High" in cpu_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n\n")
            issue += 1
            ec.append(["HI4"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n\n")
            

        # RAM TEST RESULT
        if "High" in ram_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
            issue += 1
            ec.append(["HI5"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
        
        # NETWORK TEST RESULT
        if "error" in network_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n\n")
            issue += 1
            ec.append(["SI1"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n\n")

        # # MOUSE AND KEYBOARD TEST RESULT
        # if "not" in mouse_keyboard_status or "error" in mouse_keyboard_status:
        #     self.result_text.setCurrentCharFormat(red_format)
        #     self.result_text.insertPlainText("Mouse and Keyboard Status: \t" + mouse_keyboard_status + "\n")
        #     issue += 1
        #     ec.append(["HI9"])
        # else:
        #     self.result_text.setCurrentCharFormat(blue_format)
        #     self.result_text.insertPlainText("Mouse and Keyboard Status: \t" + mouse_keyboard_status + "\n")

        #USB TEST RESULT
        if "not" in usb_status or "Error" in usb_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("USB Devices: \t" + usb_status + "\n\n")
            issue += 1
            ec.append(["HI2"])
        elif "No USB devices found." in usb_status:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("USB Devices: \t" +"USB device not found.\n\n")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("USB Devices:")
            count = 0
            for i in usb_status:
                if count == 0:
                    self.result_text.insertPlainText("\t" + i + "\n")
                else:
                    self.result_text.insertPlainText("\t\t" + i + "\n")
                count += 1
            self.result_text.insertPlainText("\n")

        # DISK TEST RESULT
        if "Disk usage is normal." in disk_result:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Disk Status: " + disk_result + "\n")
        else:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Disk Status:")
            count = 0
            for i in disk_result:
                if count == 0:
                    self.result_text.insertPlainText("\t" + i + "\n")
                else:
                    self.result_text.insertPlainText("\t\t" + i + "\n")
                count += 1
            self.result_text.insertPlainText("\n")

            issue += 1
            ec.append(["HI6"])

        # CAMERA TEST RESULT
        if "not" in camera_status or "error" in camera_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")
            issue += 1
            ec.append(["HI7"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")

        # MICROPHONE TEST RESULT
        if "not" in mic_status or "error" in mic_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")
            issue += 1
            ec.append(["HI8"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")

        #FINAL RESULT
        if issue != 0:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("\n\nPotential issues detected. \nClick on the Possible Solutions button\n")
            self.solutions_button.show()
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("All tests completed successfully.\n")
        
        self.export.show()

    def export_to_word_file_run(self):
        text = self.result_text.toPlainText()
        if text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Word File", "", "Word Files (*.docx);;All Files (*)")
            if file_path:
                document = Document()
                document.add_paragraph(text)
                document.save(file_path)

    # def fade_in_widget(self):
    #     fade_animation = QPropertyAnimation(self.fade_button, b"windowOpacity")
    #     fade_animation.setDuration(1000)
    #     fade_animation.setStartValue(0.0)
    #     fade_animation.setEndValue(1.0)
    #     self.fade_button.setVisible(True)
    #     fade_animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #0D0630; }")
    window = FixerZApp()
    window.show()
    sys.exit(app.exec_())
