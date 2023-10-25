import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QProgressBar, QFileDialog, QMessageBox, QLabel
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QPixmap, QRadialGradient, QPalette, QIcon
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
font.setPointSize(16)
font.setFamily("Poppins")
font.setBold(True)
heading.setFont(font)

sub_heading = QTextCharFormat()
sub_heading.setForeground(QColor("#e9ecef"))
font = QFont()
font.setPointSize(10)
font.setFamily("Poppins")
font.setBold(False)
sub_heading.setFont(font)

blue_format = QTextCharFormat()
blue_format.setForeground(QColor("#A3E7FC"))
font = QFont()
font.setPointSize(10)
font.setFamily("Poppins")
font.setBold(False)
blue_format.setFont(font)

red_format = QTextCharFormat()
red_format.setForeground(QColor("#ED254E"))
font = QFont()
font.setPointSize(10)
font.setFamily("Poppins")
font.setBold(False)
red_format.setFont(font)

black_format = QTextCharFormat()
black_format.setForeground(QColor("black"))

green_format = QTextCharFormat()
green_format.setForeground(QColor("#3CB043"))
font = QFont()
font.setPointSize(10)
font.setFamily("Poppins")
font.setBold(False)
green_format.setFont(font)

result_text_good = QTextCharFormat()
result_text_good.setForeground(QColor("#3CB043"))
font = QFont()
font.setPointSize(12)
font.setFamily("Poppins")
font.setBold(False)
result_text_good.setFont(font)

result_text_bad = QTextCharFormat()
result_text_bad.setForeground(QColor("#ED254E"))
font = QFont()
font.setPointSize(12)
font.setFamily("Poppins")
font.setBold(False)
result_text_bad.setFont(font)


class FixerZApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FixerZ")
        initial_width = 1200
        initial_height = int((initial_width * 9) / 16)
        self.setGeometry(100, 100, initial_width, initial_height)
        # self.setFixedSize(initial_width, initial_height)
        self.setStyleSheet("background-color: #0f1d30;")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a horizontal layout for the three columns
        self.layout = QVBoxLayout(self.central_widget)
        
        #Logo and top section
        self.logo = QHBoxLayout()
        pixmap = QPixmap("logo.png")  # Replace "logo.png" with the actual path to your logo image
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        image_width = int(screen_width * 0.07)  # 10% of the screen width
        pixmap = pixmap.scaledToWidth(image_width, Qt.SmoothTransformation)
        logo_label = QLabel(self)
        logo_label.setPixmap(pixmap)
        self.logo.addWidget(logo_label)

        #Content section
        self.content = QHBoxLayout()

        # Navigation Column
        self.navigation_container = QWidget()
        self.navigation_layout = QVBoxLayout()
        self.navigation_container.setLayout(self.navigation_layout)
        self.navigation_container.setStyleSheet("background-color: #2a2854; border: none; border-radius: 20px;")
        self.navigation_layout.setAlignment(Qt.AlignTop)
        self.navigation_container.setContentsMargins(0, 0, 0, 0)

            # Scan / Test Mode Button
        scan_icon = QIcon("images/test.png")
        self.scan_button = QPushButton()
        self.scan_button.setFixedSize(40, int(0.1 * screen_height))
        self.scan_button.setIcon(scan_icon)
        self.scan_button.setIconSize(self.scan_button.size())
        self.scan_button.setStyleSheet("background-color: transparent; border: none;")
        self.scan_button.clicked.connect(self.run_scan)

            # Solutions Button
        solutions_icon = QIcon("images/solutions.png")
        self.solutions_button = QPushButton()
        self.solutions_button.setFixedSize(40, int(0.1 * screen_height))
        self.solutions_button.setIcon(solutions_icon)
        self.solutions_button.setIconSize(self.solutions_button.size())
        self.solutions_button.setStyleSheet("background-color: transparent; color: white; font-weight: bold; border-radius: 5px; border: none")
        self.solutions_button.clicked.connect(self.fetch_possible_solutions)

        self.navigation_layout.addWidget(self.scan_button)
        self.navigation_layout.addWidget(self.solutions_button)

        # Info Column
        self.info_layout = QVBoxLayout()

            # Welcome Text
        self.welcome_text = QTextEdit()
        self.welcome_text.setStyleSheet("background-color: transparent; border: none;")
        self.welcome_text.setReadOnly(True)
        self.welcome_text.setFixedWidth(int(0.66 * screen_width))
        self.welcome_text.setFixedHeight(int(0.05 * screen_height))
        self.welcome_text.setContentsMargins(10, 10, 10, 10)
        user_name = "User"  # Replace with the actual user's name
        self.welcome_text.setCurrentCharFormat(heading)
        self.welcome_text.setText(f"Welcome {user_name}")
        self.welcome_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Tests Section and Progress Bar
        self.test_results_container = QWidget()
        self.test_results_container.setStyleSheet("background-color: #3d395f; color: white;border: none; border-radius: 20px;")
        self.test_results_container.setLayout(QHBoxLayout())
        self.test_results_container.setContentsMargins(10, 10, 10, 10)
        self.test_results_container.setFixedSize(int(0.66 * screen_width), int(0.44 * screen_height))
                #section 1
        self.section1_container = QWidget()
        self.section1_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section1_container.setLayout(QVBoxLayout())
        self.section1_container.setContentsMargins(10, 10, 10, 10)
        self.section1_container.setFixedSize(int(0.15 * screen_width), int(0.4 * screen_height))
                    #section 1 text
        self.section1_text1 = QTextEdit()
        self.section1_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section1_text1.setReadOnly(True)
        self.section1_text1.setFixedWidth(int(0.15 * screen_width))
        self.section1_text1.setFixedHeight(int(0.1 * screen_height))
        self.section1_text1.setContentsMargins(10, 10, 10, 10)
        self.section1_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section1_text1.setCurrentCharFormat(heading)
        self.section1_text1.setPlainText("Hardware Scans")
        self.section1_text1.setAlignment(Qt.AlignCenter)
                    #section 1 image
        self.section1_image = QLabel()
        self.section1_image.setPixmap(QPixmap("images/hardware.png"))
        self.section1_image.setAlignment(Qt.AlignCenter)
                    #section 1 result
        self.section1_result = QTextEdit()
        self.section1_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section1_result.setReadOnly(True)
        self.section1_result.setFixedWidth(int(0.15 * screen_width))
                    #Addition to section 1 container
        self.section1_container.layout().addWidget(self.section1_text1)
        self.section1_container.layout().addWidget(self.section1_image)
        self.section1_container.layout().addWidget(self.section1_result)
                
                #section 2
        self.section2_container = QWidget()
        self.section2_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section2_container.setLayout(QVBoxLayout())
        self.section2_container.setContentsMargins(10, 10, 10, 10)
        self.section2_container.setFixedSize(int(0.15 * screen_width), int(0.4 * screen_height))
                    #section 2 text
        self.section2_text1 = QTextEdit()
        self.section2_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section2_text1.setReadOnly(True)
        self.section2_text1.setFixedWidth(int(0.15 * screen_width))
        self.section2_text1.setFixedHeight(int(0.1 * screen_height))
        self.section2_text1.setContentsMargins(10, 10, 10, 10)
        self.section2_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section2_text1.setCurrentCharFormat(heading)
        self.section2_text1.setPlainText("Network Scans")
        self.section2_text1.setAlignment(Qt.AlignCenter)
                    #section 2 image
        self.section2_image = QLabel()
        self.section2_image.setPixmap(QPixmap("images/network.png"))
        self.section2_image.setAlignment(Qt.AlignCenter)
                    #section 2 result
        self.section2_result = QTextEdit()
        self.section2_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section2_result.setReadOnly(True)
        self.section2_result.setFixedWidth(int(0.15 * screen_width))
                    #Addition to section 2 container
        self.section2_container.layout().addWidget(self.section2_text1)
        self.section2_container.layout().addWidget(self.section2_image)
        self.section2_container.layout().addWidget(self.section2_result)        

                #section 3
        self.section3_container = QWidget()
        self.section3_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section3_container.setLayout(QVBoxLayout())
        self.section3_container.setContentsMargins(10, 10, 10, 10)
        self.section3_container.setFixedSize(int(0.15 * screen_width), int(0.4 * screen_height))
                    #section 3 text
        self.section3_text1 = QTextEdit()
        self.section3_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section3_text1.setReadOnly(True)
        self.section3_text1.setFixedWidth(int(0.15 * screen_width))
        self.section3_text1.setFixedHeight(int(0.1 * screen_height))
        self.section3_text1.setContentsMargins(10, 10, 10, 10)
        self.section3_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section3_text1.setCurrentCharFormat(heading)
        self.section3_text1.setPlainText("Memory Scans")
        self.section3_text1.setAlignment(Qt.AlignCenter)
                    #section 3 image
        self.section3_image = QLabel()
        self.section3_image.setPixmap(QPixmap("images/memory.png"))
        self.section3_image.setAlignment(Qt.AlignCenter)
                    #section 3 result
        self.section3_result = QTextEdit()
        self.section3_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section3_result.setReadOnly(True)
        self.section3_result.setFixedWidth(int(0.15 * screen_width))
                    #Addition to section 3 container
        self.section3_container.layout().addWidget(self.section3_text1)
        self.section3_container.layout().addWidget(self.section3_image)
        self.section3_container.layout().addWidget(self.section3_result)

            #section 4
        self.section4_container = QWidget()
        self.section4_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section4_container.setLayout(QVBoxLayout())
        self.section4_container.setContentsMargins(10, 10, 10, 10)
        self.section4_container.setFixedSize(int(0.15 * screen_width), int(0.4 * screen_height))
                    #section 4 text
        self.section4_text1 = QTextEdit()
        self.section4_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section4_text1.setReadOnly(True)
        self.section4_text1.setFixedWidth(int(0.15 * screen_width))
        self.section4_text1.setFixedHeight(int(0.1 * screen_height))
        self.section4_text1.setContentsMargins(10, 10, 10, 10)
        self.section4_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section4_text1.setCurrentCharFormat(heading)
        self.section4_text1.setPlainText("CPU Scans")
        self.section4_text1.setAlignment(Qt.AlignCenter)
                    #section 4 image
        self.section4_image = QLabel()
        self.section4_image.setPixmap(QPixmap("images/CPU.png"))
        self.section4_image.setAlignment(Qt.AlignCenter)
                    #section 4 result
        self.section4_result = QTextEdit()
        self.section4_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section4_result.setReadOnly(True)
        self.section4_result.setFixedWidth(int(0.15 * screen_width))
                    #Addition to section 4 container
        self.section4_container.layout().addWidget(self.section4_text1)
        self.section4_container.layout().addWidget(self.section4_image)
        self.section4_container.layout().addWidget(self.section4_result)


            #Addition of all sections to test results container
        self.test_results_container.layout().addWidget(self.section1_container)
        self.test_results_container.layout().addWidget(self.section2_container)
        self.test_results_container.layout().addWidget(self.section3_container)
        self.test_results_container.layout().addWidget(self.section4_container)


            # Result Text
        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("background-color: #3d395f; color: white;border: none; border-radius: 20px;")
        self.result_text.setReadOnly(True)
        self.result_text.setFixedSize(int(0.66 * screen_width), int(0.44 * screen_height))
        self.result_text.setContentsMargins(10, 10, 10, 10)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

            # Specs Text
        self.specs_text = QTextEdit()
        self.specs_text.setStyleSheet("background-color: #353652;border: none; border-radius: 20px;")
        self.specs_text.setReadOnly(True)
        self.specs_text.setFixedSize(int(0.66 * screen_width), int(0.31 * screen_height))
        self.specs_text.setContentsMargins(10, 10, 10, 10)
        self.specs_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
            # Add to the info layout
        self.info_layout.addWidget(self.welcome_text)
        self.info_layout.addWidget(self.test_results_container)
        self.info_layout.addWidget(self.progress_bar)
        self.info_layout.addWidget(self.specs_text)
        
        # Quick Actions Column
        self.quick_actions_layout = QVBoxLayout()
        self.run_button = QPushButton("Run Scan", self)
        self.run_button.setStyleSheet("background-color: #65B891; color: white; font-weight: bold; border-radius: 5px; border: none; min-width: 200px; max-width: 400px;min-height: 40px; max-height: 60px;")
        self.run_button.clicked.connect(self.run_scan)
        
        self.export = QPushButton("Export", self)
        self.export.setStyleSheet("background-color: #0000FF; color: white; font-weight: bold; border-radius: 5px; border: none; min-width: 200px; max-width: 400px;min-height: 40px; max-height: 60px;")
        self.export.clicked.connect(self.export_to_word_file_run)

        self.share_button = QPushButton("Share")
        self.quick_actions_layout.addWidget(self.run_button)
        self.quick_actions_layout.addWidget(self.export)
        self.quick_actions_layout.addWidget(self.share_button)

        # Add the three columns to the main layout
        self.content.addWidget(self.navigation_container)
        self.content.addLayout(self.info_layout)
        self.content.addLayout(self.quick_actions_layout)

        self.layout.addLayout(self.logo)
        self.layout.addLayout(self.content)

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
                        # view_more_button = QPushButton("View More", self)
                        # view_more_button.setStyleSheet("color: blue; text-decoration: underline;")
                        # view_more_button.clicked.connect(lambda checked, desc=solution[0]: self.view_more_clicked(desc))
                        # self.layout.addWidget(view_more_button)
                self.result_text.insertPlainText("\n")
            cursor.close()
            db_connection.close()

        except Exception as e:
            self.result_text.clear()
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText(f"Error fetching solutions: {str(e)}")

    # def view_more_clicked(self, error_description):
    #     self.search_error_solution(error_description)
    #     QMessageBox.information(self, "View More Clicked", "You clicked the 'View More' button.")

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

    # def search_error_solution(error_description):
    #     search_query = f"Step wise solution for troubleshooting {error_description}"
    #     webbrowser.open_new_tab("https://www.google.com/search?q=" + search_query)

    def run_scan(self):
        ec.clear()
        self.result_text.clear()
        self.specs_text.clear()
        self.start()

        total_tests = 7
        completed_tests = 0

        self.progress_bar.show()
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
        hardware_issue = 0
        memory_issue = 0
        network_issue = 0
        cpu_issue = 0

        self.result_text.clear()
        self.result_text.setCurrentCharFormat(heading)
        self.result_text.insertPlainText("Troubleshooting Results:\n")
        self.result_text.setCurrentCharFormat(sub_heading)
        
        # CPU TEST RESULT 
        if "High" in cpu_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n\n")
            issue += 1
            cpu_issue += 1
            ec.append(["HI4"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n\n")
            
        # RAM TEST RESULT
        if "High" in ram_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
            issue += 1
            memory_issue += 1
            ec.append(["HI5"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
        
        # NETWORK TEST RESULT
        if "error" in network_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Network Status: \t" + network_result + "\n\n")
            issue += 1
            network_issue += 1
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
            hardware_issue += 1
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
            memory_issue += 1  
            ec.append(["HI6"])

        # CAMERA TEST RESULT
        if "not" in camera_status or "error" in camera_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")
            issue += 1
            hardware_issue += 1
            ec.append(["HI7"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")

        # MICROPHONE TEST RESULT
        if "not" in mic_status or "error" in mic_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")
            issue += 1
            hardware_issue += 1
            ec.append(["HI8"])
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")

        #FINAL RESULT
        if issue != 0:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("\n\nPotential issues detected. \nCheck the Possible Solutions Section\n")
            self.solutions_button.show()
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("No issue found\n")

        #Scan Results
        if hardware_issue != 0:
            self.section1_result.setCurrentCharFormat(result_text_bad)
            self.section1_result.insertPlainText("Issues Detected")
            self.section1_result.setAlignment(Qt.AlignCenter)
        else:
            self.section1_result.setCurrentCharFormat(result_text_good)
            self.section1_result.insertPlainText("No Issues Detected")
            self.section1_result.setAlignment(Qt.AlignCenter)

        if network_issue != 0:
            self.section2_result.setCurrentCharFormat(result_text_bad)
            self.section2_result.insertPlainText("Issues Detected")
            self.section2_result.setAlignment(Qt.AlignCenter)
        else:
            self.section2_result.setCurrentCharFormat(result_text_good)
            self.section2_result.insertPlainText("No Issues Detected")
            self.section2_result.setAlignment(Qt.AlignCenter)
        
        if memory_issue != 0:
            self.section3_result.setCurrentCharFormat(result_text_bad)
            self.section3_result.insertPlainText("Issues Detected")
            self.section3_result.setAlignment(Qt.AlignCenter)
        else:
            self.section3_result.setCurrentCharFormat(result_text_good)
            self.section3_result.insertPlainText("No Issues Detected")
            self.section3_result.setAlignment(Qt.AlignCenter)
        
        if cpu_issue != 0:
            self.section4_result.setCurrentCharFormat(result_text_bad)
            self.section4_result.insertPlainText("Issues Detected")
            self.section4_result.setAlignment(Qt.AlignCenter)
        else:
            self.section4_result.setCurrentCharFormat(result_text_good)
            self.section4_result.insertPlainText("No Issues Detected")
            self.section4_result.setAlignment(Qt.AlignCenter)

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
