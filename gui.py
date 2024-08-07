import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QProgressBar, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QPixmap, QIcon, QCursor
from PyQt5.QtCore import Qt, QSize
import scan_functions
import fix_functions
import listdata
from docx import Document
import threading
import subprocess
import multiprocessing 

present_screen = 1

#List of error codes
global ec
ec = []

#convert relative address to proper resource path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Design presets for text formats

heading = QTextCharFormat()
heading.setForeground(QColor("white"))
font = QFont()
font.setPointSize(16)
font.setFamily("Poppins")
font.setBold(True)
heading.setFont(font)

heading2 = QTextCharFormat()
heading2.setForeground(QColor("white"))
font = QFont()
font.setPointSize(14)
font.setFamily("Poppins")
font.setBold(True)
heading2.setFont(font)

sub_heading = QTextCharFormat()
sub_heading.setForeground(QColor("#e9ecef"))
font = QFont()
font.setPointSize(8)
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

result_text_wait = QTextCharFormat()
result_text_wait.setForeground(QColor("#A3E7FC"))
font = QFont()
font.setPointSize(12)
font.setFamily("Poppins")
font.setBold(False)
result_text_wait.setFont(font)


class LoadingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setFixedSize(1749, 843)
        self.setWindowFlag(Qt.FramelessWindowHint)
        app_icon = QIcon(resource_path("images/logo/icon.png"))
        self.setWindowIcon(app_icon)
        image_label = QLabel(self)
        pixmap = QPixmap(resource_path("images/launcher.png"))
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        self.central_widget = QLabel()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)


class FixerZApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FixerZ")
        initial_width = 1200
        initial_height = int((initial_width * 9) / 16)
        self.setGeometry(100, 100, initial_width, initial_height)
        self.setFixedSize(1749, 843)
        self.setStyleSheet("background-color: #0f1d30;")

        app_icon = QIcon(resource_path("images/logo/icon.png"))
        self.setWindowIcon(app_icon)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a horizontal layout for the three columns
        self.layout = QVBoxLayout(self.central_widget)
        
        #Logo and top section
        self.logo = QHBoxLayout()
        pixmap = QPixmap(resource_path("images/logo.png"))
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        global screen_width 
        screen_width = screen_geometry.width()
        global screen_height 
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
        self.navigation_container.setStyleSheet("background-color: #3d395f; border: none; border-radius: 20px;")
        self.navigation_layout.setAlignment(Qt.AlignTop)
        self.navigation_container.setContentsMargins(0, 0, 0, 0)

            # Scan / Test Mode Button
        scan_icon = QIcon(resource_path("images/test_clicked.png"))
        self.scan_button = QPushButton()
        self.scan_button.setFixedSize(40, int(0.1 * screen_height))
        self.scan_button.setIcon(scan_icon)
        self.scan_button.setIconSize(self.scan_button.size())
        self.scan_button.setStyleSheet("background-color: transparent; border: none;")
        self.scan_button.clicked.connect(self.scan_button_clicked)
        self.scan_button.setCursor(QCursor(Qt.PointingHandCursor))

            # Solutions Button
        solutions_icon = QIcon(resource_path("images/solutions.png"))
        self.solutions_button = QPushButton()
        self.solutions_button.setFixedSize(40, int(0.1 * screen_height))
        self.solutions_button.setIcon(solutions_icon)
        self.solutions_button.setIconSize(self.solutions_button.size())
        self.solutions_button.setStyleSheet("background-color: transparent; color: white; font-weight: bold; border-radius: 5px; border: none")
        self.solutions_button.clicked.connect(self.solutions_button_clicked)
        self.solutions_button.setCursor(QCursor(Qt.PointingHandCursor))

            # Auto Fix Button
        auto_fix_icon = QIcon(resource_path("images/autofix.png"))
        self.auto_fix_button = QPushButton()
        self.auto_fix_button.setFixedSize(40, int(0.1 * screen_height))
        self.auto_fix_button.setIcon(auto_fix_icon)
        self.auto_fix_button.setIconSize(self.auto_fix_button.size())
        self.auto_fix_button.setStyleSheet("background-color: transparent; color: white; font-weight: bold; border-radius: 5px; border: none")
        self.auto_fix_button.clicked.connect(self.auto_fix_button_clicked)
        self.auto_fix_button.setCursor(QCursor(Qt.PointingHandCursor))

            # Add buttons to navigation layout
        self.navigation_layout.addWidget(self.scan_button)
        self.navigation_layout.addWidget(self.solutions_button)
        self.navigation_layout.addWidget(self.auto_fix_button)

        # Info Column
        self.info_layout = QVBoxLayout()

            # Welcome Text
        self.welcome_text = QTextEdit()
        self.welcome_text.setStyleSheet("background-color: transparent; border: none;")
        self.welcome_text.setReadOnly(True)
        self.welcome_text.setFixedWidth(int(0.66 * screen_width))
        self.welcome_text.setFixedHeight(int(0.05 * screen_height))
        self.welcome_text.setContentsMargins(10, 10, 10, 10)
        self.welcome_text.setCurrentCharFormat(heading)
        self.welcome_text.setText("Welcome User!")
        self.welcome_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Tests Section and Progress Bar
        self.test_results_container = QWidget()
        self.test_results_container.setStyleSheet("background-color: #3d395f; color: white;border: none; border-radius: 20px;")
        self.test_results_container.setLayout(QHBoxLayout())
        self.test_results_container.setContentsMargins(10, 10, 10, 10)
        self.test_results_container.setFixedSize(int(0.66 * screen_width), int(0.38 * screen_height))
                #section 1
        self.section1_container = QWidget()
        self.section1_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section1_container.setLayout(QVBoxLayout())
        self.section1_container.setContentsMargins(10, 10, 10, 10)
        self.section1_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
                    #section 1 text
        self.section1_text1 = QTextEdit()
        self.section1_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section1_text1.setReadOnly(True)
        self.section1_text1.setFixedHeight(int(0.1 * screen_height))
        self.section1_text1.setContentsMargins(10, 10, 10, 10)
        self.section1_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section1_text1.setCurrentCharFormat(heading)
        self.section1_text1.setPlainText("Hardware Scans")
        self.section1_text1.setAlignment(Qt.AlignCenter)
        self.section1_text1.setAlignment(Qt.AlignVCenter)
                    #section 1 image
        self.section1_image = QLabel()
        self.section1_image.setPixmap(QPixmap(resource_path("images/hardware.png")))
        self.section1_image.setAlignment(Qt.AlignCenter)
                    #section 1 result
        self.section1_result = QTextEdit()
        self.section1_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section1_result.setReadOnly(True)
        self.section1_result.setAlignment(Qt.AlignCenter)
        self.section1_result.setPlainText("Waiting for scan to start...")
                    #Addition to section 1 container
        self.section1_container.layout().addWidget(self.section1_text1)
        self.section1_container.layout().addWidget(self.section1_image)
        self.section1_container.layout().addWidget(self.section1_result)
                
                #section 2
        self.section2_container = QWidget()
        self.section2_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section2_container.setLayout(QVBoxLayout())
        self.section2_container.setContentsMargins(10, 10, 10, 10)
        self.section2_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
                    #section 2 text
        self.section2_text1 = QTextEdit()
        self.section2_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section2_text1.setReadOnly(True)
        self.section2_text1.setFixedHeight(int(0.1 * screen_height))
        self.section2_text1.setContentsMargins(10, 10, 10, 10)
        self.section2_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section2_text1.setCurrentCharFormat(heading)
        self.section2_text1.setPlainText("Network Scans")
        self.section2_text1.setAlignment(Qt.AlignCenter) 
                    #section 2 image
        self.section2_image = QLabel()
        self.section2_image.setPixmap(QPixmap(resource_path("images/network.png")))
        self.section2_image.setAlignment(Qt.AlignCenter)
                    #section 2 result
        self.section2_result = QTextEdit()
        self.section2_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section2_result.setReadOnly(True)
        self.section2_result.setAlignment(Qt.AlignCenter)
        self.section2_result.setPlainText("Waiting for scan to start...")
        self.section2_container.layout().addWidget(self.section2_text1)
        self.section2_container.layout().addWidget(self.section2_image)
        self.section2_container.layout().addWidget(self.section2_result)        

                #section 3
        self.section3_container = QWidget()
        self.section3_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section3_container.setLayout(QVBoxLayout())
        self.section3_container.setContentsMargins(10, 10, 10, 10)
        self.section3_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
                    #section 3 text
        self.section3_text1 = QTextEdit()
        self.section3_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section3_text1.setReadOnly(True)
        self.section3_text1.setFixedHeight(int(0.1 * screen_height))
        self.section3_text1.setContentsMargins(10, 10, 10, 10)
        self.section3_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section3_text1.setCurrentCharFormat(heading)
        self.section3_text1.setPlainText("Memory Scans")
        self.section3_text1.setAlignment(Qt.AlignCenter)
                    #section 3 image
        self.section3_image = QLabel()
        self.section3_image.setPixmap(QPixmap(resource_path("images/memory.png")))
        self.section3_image.setAlignment(Qt.AlignCenter)
                    #section 3 result
        self.section3_result = QTextEdit()
        self.section3_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section3_result.setReadOnly(True)
        self.section3_result.setAlignment(Qt.AlignCenter)
        self.section3_result.setPlainText("Waiting for scan to start...")
                    #Addition to section 3 container
        self.section3_container.layout().addWidget(self.section3_text1)
        self.section3_container.layout().addWidget(self.section3_image)
        self.section3_container.layout().addWidget(self.section3_result)

            #section 4
        self.section4_container = QWidget()
        self.section4_container.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.section4_container.setLayout(QVBoxLayout())
        self.section4_container.setContentsMargins(10, 10, 10, 10)
        self.section4_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
                    #section 4 text
        self.section4_text1 = QTextEdit()
        self.section4_text1.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section4_text1.setReadOnly(True)
        self.section4_text1.setFixedHeight(int(0.1 * screen_height))
        self.section4_text1.setContentsMargins(10, 10, 10, 10)
        self.section4_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.section4_text1.setCurrentCharFormat(heading)
        self.section4_text1.setPlainText("CPU Scans")
        self.section4_text1.setAlignment(Qt.AlignCenter)
                    #section 4 image
        self.section4_image = QLabel()
        self.section4_image.setPixmap(QPixmap(resource_path("images/CPU.png")))
        self.section4_image.setAlignment(Qt.AlignCenter)
                    #section 4 result
        self.section4_result = QTextEdit()
        self.section4_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.section4_result.setReadOnly(True)
        self.section4_result.setAlignment(Qt.AlignCenter)
        self.section4_result.setAlignment(Qt.AlignVCenter)
        self.section4_result.setPlainText("Waiting for scan to start...")
                    #Addition to section 4 container
        self.section4_container.layout().addWidget(self.section4_text1)
        self.section4_container.layout().addWidget(self.section4_image)
        self.section4_container.layout().addWidget(self.section4_result)


            #Addition of all sections to test results container
        self.test_results_container.layout().addWidget(self.section1_container)
        self.test_results_container.layout().addWidget(self.section2_container)
        self.test_results_container.layout().addWidget(self.section3_container)
        self.test_results_container.layout().addWidget(self.section4_container)


            # Detailed Result Text
        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("background-color: #3d395f; color: white;border: none; border-radius: 20px;")
        self.result_text.setReadOnly(True)
        self.result_text.setFixedSize(int(0.66 * screen_width), int(0.66* screen_height))
        self.result_text.setContentsMargins(10, 10, 10, 10)
        self.result_text.hide()

        #Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

            # Specs Text
        self.specs_container = QWidget()
        self.specs_container.setStyleSheet("background-color: #3d395f; color: white;border: none; border-radius: 20px;")
        self.specs_container.setLayout(QVBoxLayout())
        self.specs_container.setFixedSize(int(0.66 * screen_width), int(0.28 * screen_height))
                #Heading
        self.specs_heading = QTextEdit()
        self.specs_heading.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_heading.setReadOnly(True)
        self.specs_heading.setFixedWidth(int(0.66 * screen_width))
        self.specs_heading.setFixedHeight(int(0.03 * screen_height))
        self.specs_heading.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_heading.setCurrentCharFormat(heading2)
        self.specs_heading.setPlainText("Basic System Details")
        self.specs_heading.setAlignment(Qt.AlignCenter)
                    #Container2
        self.specs_container2 = QWidget()
        self.specs_container2.setStyleSheet("background-color: transparent; color: white;border: none; border-radius: 20px;")
        self.specs_container2.setLayout(QHBoxLayout())
        self.specs_container2.setFixedSize(int(0.66 * screen_width), int(0.26 * screen_height))
                        #Section 1
        self.specs_section1 = QWidget()
        self.specs_section1.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.specs_section1.setLayout(QVBoxLayout())
        self.specs_section1.setContentsMargins(10, 10, 10, 10)
        self.specs_section1.setFixedSize(int(0.11 * screen_width), int(0.24 * screen_height))
                            #Section 1 Text
        self.specs_section1_text = QTextEdit()
        self.specs_section1_text.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section1_text.setReadOnly(True)
        self.specs_section1_text.setFixedHeight(int(0.1 * screen_height))
        self.specs_section1_text.setContentsMargins(10, 10, 10, 10)
        self.specs_section1_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_section1_text.setCurrentCharFormat(heading2)
        self.specs_section1_text.setPlainText("Processor")
        self.specs_section1_text.setAlignment(Qt.AlignCenter)
                            #Section 1 Image
        self.specs_section1_image = QLabel()
        self.specs_section1_image.setPixmap(QPixmap(resource_path("images/processor.png")))
        self.specs_section1_image.setAlignment(Qt.AlignCenter)
                            #Section 1 Result
        self.specs_section1_result = QTextEdit()
        self.specs_section1_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section1_result.setReadOnly(True)
        self.specs_section1_result.setAlignment(Qt.AlignCenter)
        self.specs_section1_result.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                            #Addition to section 1 container
        self.specs_section1.layout().addWidget(self.specs_section1_text)
        self.specs_section1.layout().addWidget(self.specs_section1_image)
        self.specs_section1.layout().addWidget(self.specs_section1_result)
                        #Section 2
        self.specs_section2 = QWidget()
        self.specs_section2.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.specs_section2.setLayout(QVBoxLayout())
        self.specs_section2.setContentsMargins(10, 10, 10, 10)
        self.specs_section2.setFixedSize(int(0.11 * screen_width), int(0.24 * screen_height))
                            #Section 2 Text
        self.specs_section2_text = QTextEdit()
        self.specs_section2_text.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section2_text.setReadOnly(True)
        self.specs_section2_text.setFixedHeight(int(0.1 * screen_height))
        self.specs_section2_text.setContentsMargins(10, 10, 10, 10)
        self.specs_section2_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_section2_text.setCurrentCharFormat(heading2)
        self.specs_section2_text.setPlainText("RAM")
        self.specs_section2_text.setAlignment(Qt.AlignCenter)
                            #Section 2 Image
        self.specs_section2_image = QLabel()
        self.specs_section2_image.setPixmap(QPixmap(resource_path("images/ram.png")))
        self.specs_section2_image.setAlignment(Qt.AlignCenter)
                            #Section 2 Result
        self.specs_section2_result = QTextEdit()
        self.specs_section2_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section2_result.setReadOnly(True)
        self.specs_section2_result.setAlignment(Qt.AlignCenter)
                            #Addition to section 2 container
        self.specs_section2.layout().addWidget(self.specs_section2_text)
        self.specs_section2.layout().addWidget(self.specs_section2_image)
        self.specs_section2.layout().addWidget(self.specs_section2_result)
                        
                        #Section 3
        self.specs_section3 = QWidget()
        self.specs_section3.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.specs_section3.setLayout(QVBoxLayout())
        self.specs_section3.setContentsMargins(10, 10, 10, 10)
        self.specs_section3.setFixedSize(int(0.11 * screen_width), int(0.24 * screen_height))
                            #Section 3 Text
        self.specs_section3_text = QTextEdit()
        self.specs_section3_text.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section3_text.setReadOnly(True)
        self.specs_section3_text.setFixedHeight(int(0.1 * screen_height))
        self.specs_section3_text.setContentsMargins(10, 10, 10, 10)
        self.specs_section3_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_section3_text.setCurrentCharFormat(heading2)
        self.specs_section3_text.setPlainText("Display")
        self.specs_section3_text.setAlignment(Qt.AlignCenter)
                            #Section 3 Image
        self.specs_section3_image = QLabel()
        self.specs_section3_image.setPixmap(QPixmap(resource_path("images/display.png")))
        self.specs_section3_image.setFixedHeight(int(0.08 * screen_height))
        self.specs_section3_image.setAlignment(Qt.AlignCenter)
        self.specs_section3_image.setContentsMargins(10, 10, 10, 10)
                            #Section 3 Result
        self.specs_section3_result = QTextEdit()
        self.specs_section3_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section3_result.setReadOnly(True)
        self.specs_section3_result.setAlignment(Qt.AlignCenter)
                            #Addition to section 3 container
        self.specs_section3.layout().addWidget(self.specs_section3_text)
        self.specs_section3.layout().addWidget(self.specs_section3_image)
        self.specs_section3.layout().addWidget(self.specs_section3_result)

                        #Section 4
        self.specs_section4 = QWidget()
        self.specs_section4.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.specs_section4.setLayout(QVBoxLayout())
        self.specs_section4.setContentsMargins(10, 10, 10, 10)
        self.specs_section4.setFixedSize(int(0.11 * screen_width), int(0.24 * screen_height))
                            #Section 4 Text 
        self.specs_section4_text = QTextEdit()
        self.specs_section4_text.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section4_text.setReadOnly(True)
        self.specs_section4_text.setFixedHeight(int(0.1 * screen_height))
        self.specs_section4_text.setContentsMargins(10, 10, 10, 10)
        self.specs_section4_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_section4_text.setCurrentCharFormat(heading2)
        self.specs_section4_text.setPlainText("GPU")
        self.specs_section4_text.setAlignment(Qt.AlignCenter)
                            #Section 4 Image
        self.specs_section4_image = QLabel()
        self.specs_section4_image.setPixmap(QPixmap(resource_path("images/gpu.png")))
        self.specs_section4_image.setAlignment(Qt.AlignCenter)
                            #Section 4 Result
        self.specs_section4_result = QTextEdit()
        self.specs_section4_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section4_result.setReadOnly(True)
        self.specs_section4_result.setAlignment(Qt.AlignCenter)
        self.specs_section4_result.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                            #Addition to section 4 container
        self.specs_section4.layout().addWidget(self.specs_section4_text)
        self.specs_section4.layout().addWidget(self.specs_section4_image)
        self.specs_section4.layout().addWidget(self.specs_section4_result)

                        #Section 5
        self.specs_section5 = QWidget()
        self.specs_section5.setStyleSheet("background-color: #454562; color: white;border: none; border-radius: 20px;")
        self.specs_section5.setLayout(QVBoxLayout())
        self.specs_section5.setContentsMargins(10, 10, 10, 10)
        self.specs_section5.setFixedSize(int(0.11 * screen_width), int(0.24 * screen_height))
                            #Section 5 Text
        self.specs_section5_text = QTextEdit()
        self.specs_section5_text.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section5_text.setReadOnly(True)
        self.specs_section5_text.setFixedHeight(int(0.1 * screen_height))
        self.specs_section5_text.setContentsMargins(10, 10, 10, 10)
        self.specs_section5_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.specs_section5_text.setCurrentCharFormat(heading2)
        self.specs_section5_text.setPlainText("Storage")
        self.specs_section5_text.setAlignment(Qt.AlignCenter)
                            #Section 5 Image
        self.specs_section5_image = QLabel()
        self.specs_section5_image.setPixmap(QPixmap(resource_path("images/storage.png")))
        self.specs_section5_image.setAlignment(Qt.AlignCenter)
        self.specs_section5_image.setContentsMargins(10, 10, 10, 10)
                            #Section 5 Result
        self.specs_section5_result = QTextEdit()
        self.specs_section5_result.setStyleSheet("background-color: transparent; color: white;border: none;")
        self.specs_section5_result.setReadOnly(True)
        self.specs_section5_result.setAlignment(Qt.AlignCenter)
                            #Addition to section 5 container
        self.specs_section5.layout().addWidget(self.specs_section5_text)
        self.specs_section5.layout().addWidget(self.specs_section5_image)
        self.specs_section5.layout().addWidget(self.specs_section5_result)


                    #Addition to container 2
        self.specs_container2.layout().addWidget(self.specs_section1)
        self.specs_container2.layout().addWidget(self.specs_section2)
        self.specs_container2.layout().addWidget(self.specs_section3)
        self.specs_container2.layout().addWidget(self.specs_section4)
        self.specs_container2.layout().addWidget(self.specs_section5)
                    #Addition to container
        self.specs_container.layout().addWidget(self.specs_container2)

        
            # Add to the info layout
        self.info_layout.addWidget(self.welcome_text)
        self.info_layout.addWidget(self.test_results_container)
        self.info_layout.addWidget(self.result_text)
        self.info_layout.addWidget(self.progress_bar)
        self.info_layout.addWidget(self.specs_container)
        
        # Quick Actions Column
        self.quick_actions_layout = QVBoxLayout()
        
        self.specs_text = QTextEdit()
        self.specs_text.setStyleSheet("background-color: #3a5488;border: none; border-radius: 20px;")
        self.specs_text.setReadOnly(True)
        self.specs_text.setFixedSize(int(0.2 * screen_width), int(0.31 * screen_height))
        self.specs_text.setContentsMargins(10, 10, 10, 10)
            # Quick Actions Container
        self.quick_actions_container = QWidget()
        self.quick_actions_container.setStyleSheet("background-color: #3d395f;border: none; border-radius: 20px;")
        self.quick_actions_container.setLayout(QVBoxLayout())
        self.quick_actions_container.setContentsMargins(10, 10, 10, 10)
        self.quick_actions_container.setFixedWidth(int(0.2 * screen_width))
                # Run Scan
        self.run_button_container = QWidget()
        self.run_button_container.setStyleSheet("background-color: #585760; color: white; font-weight: bold; border-radius: 20px; border: none;")
        layout = QHBoxLayout()
        self.run_button = QPushButton(self)
        self.run_button.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.run_button.setText("Run Scan")
        icon = QIcon(resource_path("images/scan.png"))
        icon_size = QSize(30, 30)
        self.run_button.setIcon(icon)
        self.run_button.setIconSize(icon_size) 
        layout.addWidget(self.run_button)
        self.run_button_container.setLayout(layout)
        self.run_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.run_button.clicked.connect(self.run_scan)

                # Show Solutions Button
        self.show_solutions_container = QWidget()
        self.show_solutions_container.setStyleSheet("background-color: #585760; color: white; font-weight: bold; border-radius: 20px; border: none;")
        layout = QHBoxLayout()
        self.show_solutions = QPushButton(self)
        self.show_solutions.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.show_solutions.setText("Show Solutions")
        icon = QIcon(resource_path("images/scan.png"))
        icon_size = QSize(30, 30)
        self.show_solutions.setIcon(icon)
        self.show_solutions.setIconSize(icon_size) 
        layout.addWidget(self.show_solutions)
        self.show_solutions_container.setLayout(layout)
        self.show_solutions.setCursor(QCursor(Qt.PointingHandCursor))
        self.show_solutions.clicked.connect(self.fetch_possible_solutions)
        self.show_solutions_container.hide()
                # Expand Result Button
        self.expand_button_container = QWidget()
        self.expand_button_container.setStyleSheet("background-color: #585760; color: white; font-weight: bold; border-radius: 20px; border: none;")
        layout = QHBoxLayout()
        self.expand_button = QPushButton(self)
        self.expand_button.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.expand_button.setText("Expand Result")
        icon = QIcon(resource_path("images/expand.png"))
        icon_size = QSize(30, 30)
        self.expand_button.setIcon(icon)
        self.expand_button.setIconSize(icon_size)
        layout.addWidget(self.expand_button)
        self.expand_button_container.setLayout(layout)
        self.expand_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.expand_button.clicked.connect(self.expand_result)
                #Collapse Result Button
        self.collapse_button_container = QWidget()
        self.collapse_button_container.setStyleSheet("background-color: #585760; color: white; font-weight: bold; border-radius: 20px; border: none;")
        layout = QHBoxLayout()
        self.collapse_button = QPushButton(self)
        self.collapse_button.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.collapse_button.setText("Collapse Result")
        icon = QIcon(resource_path("images/collapse.png"))
        icon_size = QSize(30, 30)
        self.collapse_button.setIcon(icon)
        self.collapse_button.setIconSize(icon_size)
        layout.addWidget(self.collapse_button)
        self.collapse_button_container.setLayout(layout)
        self.collapse_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.collapse_button.clicked.connect(self.collapse_result)
        self.collapse_button_container.hide()
                #Export Button
        self.export_button_container = QWidget()
        self.export_button_container.setStyleSheet("background-color: #585760; color: white; font-weight: bold; border-radius: 20px; border: none;")
        layout = QHBoxLayout()
        self.export_button = QPushButton(self)
        self.export_button.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.export_button.setText("Export")
        icon = QIcon(resource_path("images/export.png"))
        icon_size = QSize(30, 30)
        self.export_button.setIcon(icon)
        self.export_button.setIconSize(icon_size)
        layout.addWidget(self.export_button)
        self.export_button_container.setLayout(layout)
        self.export_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.export_button.clicked.connect(self.export_to_word_file_run)

                #Share Button
        self.share_button = QPushButton("Share")
                # Add to quick actions
        self.quick_actions_container.layout().addWidget(self.run_button_container)
        self.quick_actions_container.layout().addWidget(self.show_solutions_container)
        self.quick_actions_container.layout().addWidget(self.expand_button_container)
        self.quick_actions_container.layout().addWidget(self.collapse_button_container)
        self.quick_actions_container.layout().addWidget(self.export_button_container)


        self.quick_actions_layout.addWidget(self.specs_text)
        self.quick_actions_layout.addWidget(self.quick_actions_container)

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

    def expand_result(self):
        self.test_results_container.hide()
        self.result_text.show()
        self.collapse_button_container.show()
        self.expand_button_container.hide()
        self.specs_container.hide()
    
    def collapse_result(self):
        self.test_results_container.show()
        self.result_text.hide()
        self.collapse_button_container.hide()
        self.expand_button_container.show()
        self.specs_container.show()

    def fetch_possible_solutions(self):
            self.result_text.clear()
            if len(ec) == 0:
                self.result_text.setCurrentCharFormat(green_format)
                self.result_text.insertPlainText("NO ISSUES FOUND")
            else:
                for i in ec:
                    solution = listdata.get_sol(i)
                    self.result_text.setCurrentCharFormat(green_format)
                    self.result_text.insertPlainText(f"{solution[0]}: ")
                    self.result_text.insertPlainText("\nPossible Solutions:\n")
                    self.result_text.insertPlainText(f"{solution[1]}\n")
                self.result_text.insertPlainText("\n")

    def start(self):  
        # get system specs (Some may work only for windows)
        try:
            hostname_result = scan_functions.check_hostname()
        except:
            hostname_result = "OS Issues"
        try: 
            users_result = scan_functions.check_users()
        except:
            users_result = "OS Issues"
        try:
            boot_result = scan_functions.calculate_boot_time_duration()
        except:
            boot_result = "OS Issues"
        try: 
            arch_result = scan_functions.check_system_architecture()
        except:
            arch_result = "OS Issues"
        try:
            load_result = scan_functions.check_system_load()
        except:
            load_result = "OS Issues"
        try:
            version_result = scan_functions.check_system_version()
        except:
            version_result = "OS Issues"
        try:
            battery_result = scan_functions.check_battery_status()
        except:
            battery_result = "OS Issues"
        

        # display system specs
        self.specs_text.setCurrentCharFormat(heading)
        self.specs_text.insertPlainText("Basic System Details:\n")
        self.specs_text.setCurrentCharFormat(sub_heading)
        self.specs_text.insertPlainText("Hostname:\t\t" + hostname_result + "\n")
        self.specs_text.insertPlainText("Logged In Users:\t" + users_result + "\n")
        # self.specs_text.insertPlainText("System Uptime:" + uptime_result + "\n")
        self.specs_text.insertPlainText("Time since last boot:\t" + boot_result + "\n")
        self.specs_text.insertPlainText("System Architecture:\t" + arch_result + "\n")
        self.specs_text.insertPlainText("System Version:\t" + version_result + "\n")
        self.specs_text.insertPlainText("System Load:\t" + load_result + "\n")
        self.specs_text.insertPlainText("Battery Status:\t" + battery_result + "\n")

        #set specs section
        try:
            cpu_info = scan_functions.get_cpu_info()
        except:
            cpu_info = "OS Issues"
        self.specs_section1_result.setCurrentCharFormat(sub_heading)
        self.specs_section1_result.setPlainText(cpu_info)

        try:
            ram_info = scan_functions.get_ram_info()
        except:
            ram_info = "OS Issues"
        self.specs_section2_result.setCurrentCharFormat(sub_heading)
        self.specs_section2_result.setPlainText(ram_info)

        try:
            display_info = scan_functions.get_display_info()
        except:
            display_info = "OS Issues"
        self.specs_section3_result.setCurrentCharFormat(sub_heading)
        self.specs_section3_result.setPlainText(display_info)

        try:
            gpu_info = scan_functions.get_gpu_info()
        except:
            gpu_info = "OS Issues"
        self.specs_section4_result.setCurrentCharFormat(sub_heading)
        self.specs_section4_result.setPlainText(gpu_info)

        try:
            storage_info = scan_functions.get_storage_info()
        except:
            storage_info = "OS Issues"
        self.specs_section5_result.setCurrentCharFormat(sub_heading)
        self.specs_section5_result.setPlainText(storage_info)

    def run_scan(self):
        self.specs_container.show()
        self.test_results_container.show()
        self.result_text.hide()
        ec.clear()
        self.result_text.clear()
        self.specs_text.clear()
        self.section1_result.clear()
        self.section2_result.clear()
        self.section3_result.clear()
        self.section4_result.clear()
        self.start()

        total_tests = 7
        completed_tests = 0

        self.section1_result.setCurrentCharFormat(result_text_wait)
        self.section1_result.insertPlainText("Running Scan...")
        self.section2_result.setCurrentCharFormat(result_text_wait)
        self.section2_result.insertPlainText("Running Scan...")
        self.section3_result.setCurrentCharFormat(result_text_wait)
        self.section3_result.insertPlainText("Running Scan...")
        self.section4_result.setCurrentCharFormat(result_text_wait)
        self.section4_result.insertPlainText("Running Scan...")

        self.result_text.insertPlainText("Checking System Status...\n")

        try:
            cpu_result = scan_functions.check_cpu_usage()
        except:
            cpu_result = "OS Issues"
        
        try:
            ram_result = scan_functions.check_ram_usage()
        except:
            ram_result = "OS Issues"
        
        try:
            disk_result = scan_functions.check_disk_usage()
        except:
            disk_result = "OS Issues"

        try:
            network_wifi_result = scan_functions.check_network_wifi_status()
        except:
            network_wifi_result = "OS Issues"
        
        try:
            network_et_result = scan_functions.check_network_et_status()
        except:
            network_et_result = "OS Issues"
        
        try:
            network_bt_result = scan_functions.check_network_bt_status()
        except:
            network_bt_result = "OS Issues"
        
        try:
            network_LAN_result = scan_functions.check_network_LAN_status()
        except:
            network_LAN_result = "OS Issues"
        
        try:
            usb_status = scan_functions.check_usb_ports()
        except:
            usb_status = "OS Issues"

        try:
            camera_status = scan_functions.check_camera()
        except:
            camera_status = "OS Issues"
        
        try:
            mic_status = scan_functions.check_microphone()
        except:
            mic_status = "OS Issues"
        
        self.result_text.setMinimumHeight(525)

        # Check the number of issues
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
            ec.append("HI4")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("CPU Status: \t" + cpu_result + "\n\n")
            
        # RAM TEST RESULT
        if "High" in ram_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
            issue += 1
            memory_issue += 1
            ec.append("HI5")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("RAM Status: \t" + ram_result + "\n\n")
        
        # Wi-Fi TEST RESULT
        if "not" in network_wifi_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Wi-Fi Status: \t" + network_wifi_result + "\n\n")
            issue += 1
            network_issue += 1
            ec.append("SI1")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Wi-Fi Status: \t" + network_wifi_result + "\n\n")

        # Bluetooth TEST RESULT
        if "not" in network_bt_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Bluetooth Status: \t" + network_bt_result + "\n\n")
            issue += 1
            network_issue += 1
            ec.append("SI3")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Bluetooth Status: \t" + network_bt_result + "\n\n")

        # Ethernet TEST RESULT
        if "not" in network_et_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Ethernet Status: \t" + network_et_result + "\n\n")
            issue += 1
            network_issue += 1
            ec.append("SI2")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Ethernet Status: \t" + network_et_result + "\n\n")

        # LAN TEST RESULT
        if "not" in network_LAN_result:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("LAN Status: \t" + network_LAN_result + "\n\n")
            issue += 1
            network_issue += 1
            ec.append("SI4")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("LAN Status: \t" + network_LAN_result + "\n\n")
        
        #USB TEST RESULT
        if "not" in usb_status or "Error" in usb_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("USB Devices: \t" + usb_status + "\n\n")
            issue += 1
            hardware_issue += 1
            ec.append("HI2")
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
            self.result_text.insertPlainText("Disk Status: " + str(disk_result) + "\n")
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
            ec.append("HI6")

        # CAMERA TEST RESULT
        if "not" in camera_status or "error" in camera_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")
            issue += 1
            hardware_issue += 1
            ec.append("HI7")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Camera Status: \t" + camera_status + "\n\n")

        # MICROPHONE TEST RESULT
        if "not" in mic_status or "error" in mic_status:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")
            issue += 1
            hardware_issue += 1
            ec.append("HI8")
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("Microphone Status: \t" + mic_status + "\n\n")

        #FINAL RESULT
        if issue != 0:
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Potential issues detected. \nCheck the Possible Solutions Section\n")
            self.solutions_button.show()
        elif mic_status == "OS Issues" or camera_status == "OS Issues" or usb_status == "OS Issues" or network_wifi_result == "OS Issues" or disk_result == "OS Issues" or ram_result == "OS Issues" or cpu_result == "OS Issues" or network_bt_result == "OS Issues" or network_et_result == "OS Issues" or network_LAN_result == "OS Issues":
            self.result_text.setCurrentCharFormat(red_format)
            self.result_text.insertPlainText("Some tests were not completed. This may be due to a conflicting OS or limitations of the function. Sorry Uwu\n")
            self.solutions_button.show()
        else:
            self.result_text.setCurrentCharFormat(blue_format)
            self.result_text.insertPlainText("No issue found\n")

        self.section1_result.clear()
        self.section2_result.clear()
        self.section3_result.clear()
        self.section4_result.clear()

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
    
    def scan_button_clicked(self):
        auto_fix_icon = QIcon(resource_path("images/autofix.png"))
        self.auto_fix_button.setFixedSize(40, int(0.1 * screen_height))
        self.auto_fix_button.setIcon(auto_fix_icon)
        solutions_icon = QIcon(resource_path("images/solutions.png"))
        self.solutions_button.setFixedSize(40, int(0.1 * screen_height))
        self.solutions_button.setIcon(solutions_icon)
        scan_icon = QIcon(resource_path("images/test_clicked.png"))
        self.scan_button.setFixedSize(40, int(0.1 * screen_height))
        self.scan_button.setIcon(scan_icon)
        global present_screen
        if present_screen == 2:
            present_screen = 1
            self.test_results_container.show()
            self.result_text.hide()
            self.expand_button_container.show()
            self.specs_container.show()
            self.run_button_container.show()
            self.show_solutions_container.hide()

            self.welcome_text.clear()
            self.welcome_text.setCurrentCharFormat(heading)
            self.welcome_text.setText("Welcome User!")

            self.section1_text1.clear()
            self.section1_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section1_text1.setFixedHeight(int(0.1 * screen_height))
            self.section1_text1.setContentsMargins(10, 10, 10, 10)
            self.section1_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section1_text1.setCurrentCharFormat(heading)
            self.section1_text1.setPlainText("Hardware Scans")
            self.section1_text1.setAlignment(Qt.AlignCenter)
            self.section1_image.setPixmap(QPixmap(resource_path("images/hardware.png")))
            self.section1_image.setAlignment(Qt.AlignCenter)
            self.section1_result.show()
            try:
                self.section1_run_button.hide()
            except:
                pass
            try:
                self.section1_set_button.hide()
            except:
                pass

            self.section2_text1.clear()
            self.section2_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section2_text1.setFixedHeight(int(0.1 * screen_height))
            self.section2_text1.setContentsMargins(10, 10, 10, 10)
            self.section2_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section2_text1.setCurrentCharFormat(heading)
            self.section2_text1.setPlainText("Network Scans")
            self.section2_text1.setAlignment(Qt.AlignCenter)
            self.section2_image.setPixmap(QPixmap(resource_path("images/network.png")))
            self.section2_image.setAlignment(Qt.AlignCenter)
            self.section2_result.show()
            try:
                self.section2_run_button.hide()
            except:
                pass
            try:
                self.section2_set_button.hide()
            except:
                pass

            self.section3_text1.clear()
            self.section3_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section3_text1.setFixedHeight(int(0.1 * screen_height))
            self.section3_text1.setContentsMargins(10, 10, 10, 10)
            self.section3_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section3_text1.setCurrentCharFormat(heading)
            self.section3_text1.setPlainText("Memory Scans")
            self.section3_text1.setAlignment(Qt.AlignCenter)
            self.section3_image.setPixmap(QPixmap(resource_path("images/memory.png")))
            self.section3_image.setAlignment(Qt.AlignCenter)
            self.section3_result.show()
            try:
                self.section3_set_button1.hide()
                self.section3_set_button2.hide()
            except:
                pass
            self.section4_container.show()

        elif present_screen == 3:
            present_screen = 1 
            self.welcome_text.clear()
            self.welcome_text.setCurrentCharFormat(heading)
            self.welcome_text.setText("Welcome User!")

            self.expand_button_container.show()

            self.section1_text1.clear()
            self.section1_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section1_text1.setFixedHeight(int(0.1 * screen_height))
            self.section1_text1.setContentsMargins(10, 10, 10, 10)
            self.section1_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section1_text1.setCurrentCharFormat(heading)
            self.section1_text1.setPlainText("Hardware Scans")
            self.section1_text1.setAlignment(Qt.AlignCenter)
            self.section1_image.setPixmap(QPixmap(resource_path("images/hardware.png")))
            self.section1_image.setAlignment(Qt.AlignCenter)
            self.section1_result.show()
            try:
                self.section1_run_button.hide()
            except:
                pass
            try:
                self.section1_set_button.hide()
            except:
                pass

            self.section2_text1.clear()
            self.section2_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section2_text1.setFixedHeight(int(0.1 * screen_height))
            self.section2_text1.setContentsMargins(10, 10, 10, 10)
            self.section2_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section2_text1.setCurrentCharFormat(heading)
            self.section2_text1.setPlainText("Network Scans")
            self.section2_text1.setAlignment(Qt.AlignCenter)
            self.section2_image.setPixmap(QPixmap(resource_path("images/network.png")))
            self.section2_image.setAlignment(Qt.AlignCenter)
            self.section2_result.show()
            try:
                self.section2_run_button.hide()
            except:
                pass
            try:
                self.section2_set_button.hide()
            except:
                pass

            self.section3_text1.clear()
            self.section3_container.setFixedSize(int(0.15 * screen_width), int(0.34 * screen_height))
            self.section3_text1.setFixedHeight(int(0.1 * screen_height))
            self.section3_text1.setContentsMargins(10, 10, 10, 10)
            self.section3_text1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.section3_text1.setCurrentCharFormat(heading)
            self.section3_text1.setPlainText("Memory Scans")
            self.section3_text1.setAlignment(Qt.AlignCenter)
            self.section3_image.setPixmap(QPixmap(resource_path("images/memory.png")))
            self.section3_image.setAlignment(Qt.AlignCenter)
            self.section3_result.show()
            self.section3_set_button1.hide()
            self.section3_set_button2.hide()
            
            self.section4_container.show()

    def auto_fix_button_clicked(self):
        global present_screen
        auto_fix_icon = QIcon(resource_path(resource_path("images/autofix_clicked.png")))
        self.auto_fix_button.setFixedSize(40, int(0.1 * screen_height))
        self.auto_fix_button.setIcon(auto_fix_icon)
        solutions_icon = QIcon(resource_path("images/solutions.png"))
        self.solutions_button.setFixedSize(40, int(0.1 * screen_height))
        self.solutions_button.setIcon(solutions_icon)
        scan_icon = QIcon(resource_path("images/test.png"))
        self.scan_button.setFixedSize(40, int(0.1 * screen_height))
        self.scan_button.setIcon(scan_icon)
        if present_screen == 2:
            present_screen = 3
            self.welcome_text.clear()
            self.welcome_text.setCurrentCharFormat(heading)
            self.welcome_text.setText("Quick Fixes")
            self.test_results_container.show()
            self.result_text.hide()
            self.expand_button_container.hide()
            self.collapse_button_container.hide()
            self.specs_container.show()
            self.run_button_container.show()
            self.show_solutions_container.hide()

            self.section1_text1.clear()
            self.section1_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section1_text1.setPlainText("Clear Cache")
            self.section1_text1.setAlignment(Qt.AlignCenter)
            self.section1_text1.setFixedHeight(int(0.1 * screen_height))
            self.section1_image.setPixmap(QPixmap(resource_path("images/cache.png")))
            self.section1_image.setAlignment(Qt.AlignCenter)
            self.section1_result.hide()
            self.section1_set_button = QPushButton("Set Files")
            self.section1_set_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section1_set_button.clicked.connect(self.cache_settings_set_button_clicked)
            self.section1_container.layout().addWidget(self.section1_set_button)

            self.section2_text1.clear()
            self.section2_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section2_text1.setPlainText("Disk Fragmentation")
            self.section2_text1.setAlignment(Qt.AlignCenter)
            self.section2_text1.setFixedHeight(int(0.1 * screen_height))
            self.section2_image.setPixmap(QPixmap(resource_path("images/defrag.png")))
            self.section2_image.setAlignment(Qt.AlignCenter)
            self.section2_result.hide()
            self.section2_set_button = QPushButton("Analyse Disk")
            self.section2_set_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section2_set_button.clicked.connect(self.disk_analyse_button_clicked)
            self.section2_container.layout().addWidget(self.section2_set_button)

            self.section3_text1.clear()
            self.section3_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section3_text1.setPlainText("Windows Scan")
            self.section3_text1.setAlignment(Qt.AlignCenter)
            self.section3_text1.setFixedHeight(int(0.1 * screen_height))
            self.section3_image.setPixmap(QPixmap(resource_path("images/windows_scan.png")))
            self.section3_image.setAlignment(Qt.AlignCenter)
            self.section3_result.hide()
            self.section3_set_button1 = QPushButton("Run Quick Scan")
            self.section3_set_button1.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section3_set_button1.clicked.connect(self.windows_run_quick_scan)
            self.section3_set_button2 = QPushButton("Run Full Scan")
            self.section3_set_button2.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section3_set_button2.clicked.connect(self.confirm_and_run_full_scan)   
            self.section3_container.layout().addWidget(self.section3_set_button1)
            self.section3_container.layout().addWidget(self.section3_set_button2)

            self.section4_container.hide()

        if present_screen == 1:
            present_screen = 3 
            self.welcome_text.clear()
            self.welcome_text.setCurrentCharFormat(heading)
            self.welcome_text.setText("Quick Fixes")
            self.section1_text1.clear()
            self.section1_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section1_text1.setPlainText("Clear Cache")
            self.section1_text1.setAlignment(Qt.AlignCenter)
            self.section1_text1.setFixedHeight(int(0.1 * screen_height))
            self.section1_image.setPixmap(QPixmap(resource_path("images/cache.png")))
            self.section1_image.setAlignment(Qt.AlignCenter)
            self.section1_result.hide()
            self.section1_set_button = QPushButton("Set Files")
            self.section1_set_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section1_set_button.clicked.connect(self.cache_settings_set_button_clicked)
            self.section1_container.layout().addWidget(self.section1_set_button)

            self.section2_text1.clear()
            self.section2_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section2_text1.setPlainText("Disk Fragmentation")
            self.section2_text1.setAlignment(Qt.AlignCenter)
            self.section2_text1.setFixedHeight(int(0.1 * screen_height))
            self.section2_image.setPixmap(QPixmap(resource_path("images/defrag.png")))
            self.section2_image.setAlignment(Qt.AlignCenter)
            self.section2_result.hide()
            self.section2_set_button = QPushButton("Analyse Disk")
            self.section2_set_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section2_set_button.clicked.connect(self.disk_analyse_button_clicked)
            self.section2_container.layout().addWidget(self.section2_set_button)

            self.section3_text1.clear()
            self.section3_container.setFixedSize(int(0.20 * screen_width), int(0.34 * screen_height))
            self.section3_text1.setPlainText("Windows Scan")
            self.section3_text1.setAlignment(Qt.AlignCenter)
            self.section3_text1.setFixedHeight(int(0.1 * screen_height))
            self.section3_image.setPixmap(QPixmap(resource_path("images/windows_scan.png")))
            self.section3_image.setAlignment(Qt.AlignCenter)
            self.section3_result.hide()
            self.section3_set_button1 = QPushButton("Run Quick Scan")
            self.section3_set_button1.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section3_set_button1.clicked.connect(self.windows_run_quick_scan)
            self.section3_set_button2 = QPushButton("Run Full Scan")
            self.section3_set_button2.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
            self.section3_set_button2.clicked.connect(self.confirm_and_run_full_scan)   
            self.section3_container.layout().addWidget(self.section3_set_button1)
            self.section3_container.layout().addWidget(self.section3_set_button2)

            self.section4_container.hide()

    def solutions_button_clicked(self):
        global present_screen
        auto_fix_icon = QIcon(resource_path("images/autofix.png"))
        self.auto_fix_button.setFixedSize(40, int(0.1 * screen_height))
        self.auto_fix_button.setIcon(auto_fix_icon)
        solutions_icon = QIcon(resource_path("images/solutions_clicked.png"))
        self.solutions_button.setFixedSize(40, int(0.1 * screen_height))
        self.solutions_button.setIcon(solutions_icon)
        scan_icon = QIcon(resource_path("images/test.png"))
        self.scan_button.setFixedSize(40, int(0.1 * screen_height))
        self.scan_button.setIcon(scan_icon)
        if present_screen != 2:
            present_screen = 2
            self.welcome_text.clear()
            self.welcome_text.setCurrentCharFormat(heading)
            self.welcome_text.setText("Solutions")
            self.test_results_container.hide()
            self.result_text.show()
            self.expand_button_container.hide()
            self.collapse_button_container.hide()
            self.specs_container.hide()
            self.result_text.clear()
            self.result_text.setCurrentCharFormat(sub_heading)
            self.result_text.insertPlainText("Click on the Solutions Button")
            self.run_button_container.hide()
            self.show_solutions_container.show()

    def cache_settings_set_button_clicked(self):
        try:
            result = fix_functions.disk_cleanup_setup(1)
            if "error" in result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Error Occurred")
                msg_box.setText("Sorry, Contact the Developers UwU")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Success")
                msg_box.setText("You can now delete the cache with Disk Cleanup")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "color: white;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
                self.section1_run_button = QPushButton("Clear Cache")
                self.section1_run_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
                self.section1_run_button.clicked.connect(self.cache_settings_run_button_clicked)
                self.section1_container.layout().addWidget(self.section1_run_button)
        except:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error Occurred")
            msg_box.setText("Sorry,You may not be using Windows OS or some other error may be preventing this function from executing")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()

    def cache_settings_run_button_clicked(self):
        try:
            result = fix_functions.disk_cleanup(1)
            if "error" in result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Error Occurred")
                msg_box.setText("Sorry, Contact the Developers UwU")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Success")
                msg_box.setText("Cache Cleared Successfully")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "color: white;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
        except:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error Occurred")
            msg_box.setText("Sorry,You may not be using Windows OS or some other error may be preventing this function from executing")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()

        
    def disk_analyse_button_clicked(self):
        try:
            result = fix_functions.analyze_all_drives()
            if "failure" in result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Error Occurred")
                msg_box.setText("Sorry, Contact the Developers UwU")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Success")
                msg_box.setText("All Disks Analyzed Successfully")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "color: white;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
                self.section2_run_button = QPushButton("Defragment Disk")
                self.section2_run_button.setStyleSheet("color: white;background-color: #3a5488;border: none; border-radius: 20px;height: 30px;")
                self.section2_run_button.clicked.connect(self.disk_defrag_run_button_clicked)
                self.section2_container.layout().addWidget(self.section2_run_button)
        except:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error Occurred")
            msg_box.setText("Sorry,You may not be using Windows OS or some other error may be preventing this function from executing")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()

    def disk_defrag_run_button_clicked(self):
        try:
            result = fix_functions.defragment_all_drives()
            if "failure" in result:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Error Occurred")
                msg_box.setText("Sorry, Contact the Developers UwU")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
            else:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Success")
                msg_box.setText("Disk Defragmented Successfully")
                msg_box.setStyleSheet(
                    "QMessageBox {"
                    "background-color: #F2F2F2;"
                    "}"
                    "QMessageBox QLabel {"
                    "color: #333333;"
                    "font-size: 14px;"
                    "}"
                    "QMessageBox QPushButton {"
                    "background-color: #007ACC;"
                    "color: white;"
                    "border: 1px solid #007ACC;"
                    "border-radius: 10px;"
                    "width: 100px;"
                    "height: 30px;"
                    "}"
                    "QMessageBox QPushButton:hover {"
                    "background-color: #005EAD;"
                    "color: white;"
                    "}"
                )
                msg_box.addButton("Ok", QMessageBox.AcceptRole)
                msg_box.exec_()
        except:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error Occurred")
            msg_box.setText("Sorry,You may not be using Windows OS or some other error may be preventing this function from executing")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()

    def windows_run_quick_scan(self):
        scan_message_box = QMessageBox(self)
        scan_message_box.setWindowTitle("Scan Running")
        scan_message_box.setText("The scan is in progress. Please wait. \nThis may take some time")
        scan_message_box.setStandardButtons(QMessageBox.NoButton)
        scan_message_box.setModal(True)
        scan_message_box.setStyleSheet(
            "QMessageBox {"
            "background-color: #F2F2F2;"
            "}"
            "QMessageBox QLabel {"
            "font-size: 14px;"
            "background-color: #F2F2F2;"
            "color: #333333;"
            "}"
        )
        def close_message_box():
            scan_message_box.accept()
        def run_scan():
            command = '"%ProgramFiles%\\Windows Defender\\MpCmdRun.exe" -Scan -ScanType 1'
            try:
                subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run("start ms-settings:windowsdefender", shell=True)
            except Exception as e:
                result = f"An error occurred during the scan: {e}"
            else:
                result = "Scan completed successfully"
            finally:
                close_message_box()
                self.handle_scan_result(result)
        
        scan_thread = threading.Thread(target=run_scan)
        scan_thread.start()
        scan_message_box.exec_()

    def handle_scan_result(self, result):
        if "error" in result:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error Occurred")
            msg_box.setText("Sorry, Contact the Developers UwU")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Success")
            msg_box.setText("Scan Completed Successfully")
            msg_box.setStyleSheet(
                "QMessageBox {"
                "background-color: #F2F2F2;"
                "}"
                "QMessageBox QLabel {"
                "color: #333333;"
                "font-size: 14px;"
                "}"
                "QMessageBox QPushButton {"
                "background-color: #007ACC;"
                "color: white;"
                "border: 1px solid #007ACC;"
                "border-radius: 10px;"
                "width: 100px;"
                "height: 30px;"
                "}"
                "QMessageBox QPushButton:hover {"
                "background-color: #005EAD;"
                "color: white;"
                "}"
            )
            msg_box.addButton("Ok", QMessageBox.AcceptRole)
            msg_box.exec_()

    def confirm_and_run_full_scan(self):
        confirm_message_box = QMessageBox(self)
        confirm_message_box.setWindowTitle("Warning")
        confirm_message_box.setText("Running a full scan may take a long time.\nDo you want to continue?")
        
        # Add "Yes" button with a custom background color
        yes_button = confirm_message_box.addButton(QMessageBox.Yes)
        yes_button.setStyleSheet("background-color: #007ACC; color: white;")

        # Add "No" button with a custom background color
        no_button = confirm_message_box.addButton(QMessageBox.No)
        no_button.setStyleSheet("background-color: #FF0000; color: white;")

        confirm_message_box.setStyleSheet(
            "QMessageBox {"
            "background-color: #F2F2F2;"
            "}"
            "QMessageBox QLabel {"
            "font-size: 14px;"
            "background-color: #F2F2F2;"
            "color: #333333;"
            "}"
        )
        result = confirm_message_box.exec_()
        if result == QMessageBox.Yes:
            self.run_full_scan()

    def windows_run_full_scan(self):
        scan_message_box = QMessageBox(self)
        scan_message_box.setWindowTitle("Scan Running")
        scan_message_box.setText("The scan is in progress. Please wait.")
        scan_message_box.setStandardButtons(QMessageBox.NoButton)
        scan_message_box.setModal(True)
        scan_message_box.setStyleSheet(
            "QMessageBox {"
            "background-color: #F2F2F2;"
            "}"
            "QMessageBox QLabel {"
            "font-size: 14px;"
            "background-color: #F2F2F2;"
            "color: #333333;"
            "}"
        )
        def close_message_box():
            scan_message_box.accept()
        def run_scan():
            command = '"%ProgramFiles%\\Windows Defender\\MpCmdRun.exe" -Scan -ScanType 2'
            try:
                subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run("start ms-settings:windowsdefender", shell=True)
            except Exception as e:
                result = f"An error occurred during the scan: {e}"
            else:
                result = "Scan completed successfully"
            finally:
                close_message_box()
                self.handle_scan_result(result)
        
        scan_thread = threading.Thread(target=run_scan)
        scan_thread.start()
        scan_message_box.exec_()


if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)
    
    # Show the loading screen
    loading_screen = LoadingScreen()
    loading_screen.show()
    
    # Initialize and show the main application window
    window = FixerZApp()

    # Close the loading screen when the main window is ready
    loading_screen.close()
    
    window.show()

    sys.exit(app.exec_())