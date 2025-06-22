import sys
import math
import os
import numpy as np
import pandas as pd
import time
import random

from PIL import Image, ImageQt
from datetime import datetime
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as XLImage
from drawing_metrics_logger import DrawingMetricsLogger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5 import *


class CursorSelectionScreen(QWidget):
    def __init__(self, player_name):
        super().__init__()
        self.player_name = player_name
        self.selected_cursor_pixmap = None
        self.setWindowTitle("Choose Your Cursor")
        self.setMinimumSize(2000, 1100)
        self.resize(2000, 1100)

        # Set background color
        self.setStyleSheet("background-color: #2c3e50;")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel(f"Choose Your Cursor, {self.player_name}!")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("color: white; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Cursor selection grid
        cursor_layout = QGridLayout()
        cursor_widget = QWidget()
        cursor_widget.setLayout(cursor_layout)

        cursor_files = ["C1.png", "C2.png", "C3.png", "C4.png", "C5.png","C6.png"]
        color_list = ["FF6B6B", "4ECDC4", "FFE66D", "95E1D3", "3498DB", "E9C9C4"]

        for i, cursor_file in enumerate(cursor_files):
            btn = QPushButton()
            btn.setFixedSize(400, 400)

            # Load and set icon
            icon = QIcon(cursor_file)
            if icon.isNull():
                print(f"Warning: '{cursor_file}' not found or could not be loaded.")
            btn.setIcon(icon)
            btn.setIconSize(QSize(350, 350))  # Size inside the button

            # Style the button
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 3px solid #34495e;
                    border-radius: 200px;
                    background-color: #{color_list[i]};
                }}
                QPushButton:hover {{
                    border: 5px solid #e74c3c;
                }}
                QPushButton:pressed {{
                    background-color: #2c3e50;
                }}
            """)

            btn.clicked.connect(lambda checked, file=cursor_file: self.select_cursor(file))

            row = i // 3
            col = i % 3
            cursor_layout.addWidget(btn, row, col)

        layout.addWidget(cursor_widget)

        # Next button
        self.next_btn = QPushButton("Next")
        self.next_btn.setFont(QFont("Arial", 18))
        self.next_btn.setFixedSize(200, 60)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.open_main_dialog)
        layout.addWidget(self.next_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def select_cursor(self, cursor_file):
        # Load cursor pixmap
        pixmap = QPixmap(cursor_file)
        if pixmap.isNull():
            # Create fallback image
            pixmap = QPixmap(40, 40)
            pixmap.fill(Qt.black)
            print(f"Warning: '{cursor_file}' not found, using fallback cursor.")

        self.selected_cursor_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.next_btn.setEnabled(True)



    def proceed_to_game(self):
        self.setCursor(QCursor(self.selected_cursor_pixmap))

    def open_main_dialog(self):
        self.setCursor(QCursor(self.selected_cursor_pixmap))
        self.hide()
        self.dialog = QDialog()
        self.ui = Ui_Dialog()
        # Call setupUi with the required parameters
        self.ui.setupUi(self.dialog, self.player_name, self.selected_cursor_pixmap)
        self.dialog.exec_()


class Ui_Dialog(object):
    def setupUi(self, Dialog, player_name):
        self.Dialog = Dialog
        self.player_name = player_name

        Dialog.setObjectName("Dialog")
        Dialog.resize(2000, 1100)
        Dialog.setWindowTitle(f"Game Menu - Welcome {player_name}!")


        self.label = QLabel("Pick your level to start",Dialog)
        self.label.setFont(QFont("Fantasy"))
        self.label.setStyleSheet("color: white;font-size: 80px;text-align: center;font-weight: bold;background-color: #274e13;")
        self.label.setMinimumSize(2000,100)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(0,0)





        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 150, 400, 400))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 150, 400, 400))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #6aa84f;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(1020, 150, 400, 400))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(1470, 150, 400, 400))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e73c82;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(120, 650, 400, 400))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #a13ce7;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(570, 650, 400, 400))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e7a13c;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(1020, 650, 400, 400))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #3d6d61;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.setGeometry(QtCore.QRect(1470, 650, 400, 400))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #22299d;
                color: white;
                font-weight: bold;
                font-size: 70px;
            }
        """)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.open_Level1Screen)
        self.pushButton_2.clicked.connect(self.open_Level2Screen)
        self.pushButton_3.clicked.connect(self.open_Level3Screen)
        self.pushButton_4.clicked.connect(self.open_Level4Screen)
        self.pushButton_5.clicked.connect(self.open_Level5Screen)
        self.pushButton_6.clicked.connect(self.open_Level6Screen)
        self.pushButton_7.clicked.connect(self.open_Level7Screen)
        self.pushButton_8.clicked.connect(self.open_Level8Screen)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", f"Main Menu - {self.player_name}"))
        self.pushButton.setText(_translate("Dialog", "Level 1"))
        self.pushButton_2.setText(_translate("Dialog", "Level 2"))
        self.pushButton_3.setText(_translate("Dialog", "Level 3"))
        self.pushButton_4.setText(_translate("Dialog", "Level 4"))
        self.pushButton_5.setText(_translate("Dialog", "Level 5"))
        self.pushButton_6.setText(_translate("Dialog", "Level 6"))
        self.pushButton_7.setText(_translate("Dialog", "Level 7"))
        self.pushButton_8.setText(_translate("Dialog", "Level 8"))




    def open_Level1Screen(self):
        self.Dialog.hide()
        self.cursor_selection_screen = CursorSelectionScreen(self.player_name)

        def on_next_clicked():
            cursor_pixmap = self.cursor_selection_screen.selected_cursor_pixmap
            self.cursor_selection_screen.hide()
            self.pen_screen = Level1_Screen(self.Dialog, self.player_name, cursor_pixmap)
            self.pen_screen.show()

        self.cursor_selection_screen.next_btn.clicked.disconnect()
        self.cursor_selection_screen.next_btn.clicked.connect(on_next_clicked)
        self.cursor_selection_screen.show()
    def open_Level2Screen(self):
        self.Dialog.hide()
        self.cursor_selection_screen = CursorSelectionScreen(self.player_name)

        def on_next_clicked():
            cursor_pixmap = self.cursor_selection_screen.selected_cursor_pixmap
            self.cursor_selection_screen.hide()
            self.pen_screen = Level2_Screen(self.Dialog, self.player_name, cursor_pixmap)
            self.pen_screen.show()

        self.cursor_selection_screen.next_btn.clicked.disconnect()
        self.cursor_selection_screen.next_btn.clicked.connect(on_next_clicked)
        self.cursor_selection_screen.show()
    def open_Level3Screen(self):
        self.pen_screen = Level3_Screen(self.Dialog, self.player_name)
        self.Dialog.hide()
        self.pen_screen.show()
    def open_Level4Screen(self):
        self.Dialog.hide()
        self.cursor_selection_screen = CursorSelectionScreen(self.player_name)

        def on_next_clicked():
            cursor_pixmap = self.cursor_selection_screen.selected_cursor_pixmap
            self.cursor_selection_screen.hide()
            self.pen_screen = Level4_Screen(self.Dialog, self.player_name, cursor_pixmap)
            self.pen_screen.show()

        self.cursor_selection_screen.next_btn.clicked.disconnect()
        self.cursor_selection_screen.next_btn.clicked.connect(on_next_clicked)
        self.cursor_selection_screen.show()
    def open_Level5Screen(self):
        self.pen_screen = Level5_Screen(self.Dialog, self.player_name)
        self.Dialog.hide()
        self.pen_screen.show()
    def open_Level6Screen(self):
        self.pen_screen = Level6_Screen(self.Dialog, self.player_name)
        self.Dialog.hide()
        self.pen_screen.show()
    def open_Level7Screen(self):
        self.pen_screen = Level7_Screen(self.Dialog, self.player_name)
        self.Dialog.hide()
        self.pen_screen.show()
    def open_Level8Screen(self):
        self.pen_screen = Level8_Screen(self.Dialog, self.player_name)
        self.Dialog.hide()
        self.pen_screen.show()



class Level1_Screen(QWidget):
    def __init__(self, main_dialog, player_name, cursor_pixmap):
        super().__init__()
        self.player_name = player_name
        self.main_dialog = main_dialog
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.setWindowTitle("Level 1")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)

        # Set the selected cursor (scaled for gameplay)
        cursor_for_game = cursor_pixmap.scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setCursor(QCursor(cursor_for_game))

        self.reference_layer = QPixmap(self.size())  # Wave layer
        self.reference_layer.fill(Qt.transparent)

        # Start with green background during drawing
        self.drawing = QPixmap(self.size())  # User layer
        self.drawing.fill(Qt.darkGreen)

        self.last_point = None
        self.last_time = None

        # Timing variables
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.last_pen_up_time = None  # Track when pen was last lifted

        # Data collection variables
        self.pressure_readings = []
        self.pen_positions = []
        self.pen_timestamps = []
        self.pendown_count = 0

        self._setup_ui()
        self.draw_sin_wave()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.handle_next)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.label = QLabel(f"Level 1 - Welcome {self.player_name}")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def is_in_drawing_area(self, pos):
        """Returns True if pos is NOT inside the Next button rect."""
        btn_rect = self.next_btn.geometry()
        return not btn_rect.contains(pos)

    def draw_sin_wave(self):
        """Draw the reference sine wave."""
        painter = QPainter(self.reference_layer)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        amplitude = height // 7
        mid_y = height // 2

        prev_point = (0, mid_y)
        for x in range(1, width):
            y = mid_y - int(math.sin(x * 0.01) * amplitude)
            curr_point = (x, y)
            painter.drawLine(prev_point[0], prev_point[1], curr_point[0], curr_point[1])
            prev_point = curr_point

    def handle_next(self):
        """Handle next button click."""
        self.end_time = time.time()
        self.save_image_and_log()
        self.show_popup_with_home()

    def save_image_and_log(self):
        """Save the drawing and log all metrics using the metrics logger."""
        try:
            # Create a copy of the drawing with white background for final processing
            final_drawing = QPixmap(self.drawing.size())
            final_drawing.fill(Qt.white)  # White background for final image

            # Create a painter to copy only the drawn lines (not the background)
            painter = QPainter(final_drawing)

            # Create a mask to identify the drawn areas (non-green pixels)
            temp_image = self.drawing.toImage()
            green_color = QColor(Qt.darkGreen).rgb()

            # Paint the drawing onto white background, converting green to white
            for y in range(temp_image.height()):
                for x in range(temp_image.width()):
                    pixel_color = temp_image.pixel(x, y)
                    if pixel_color != green_color:  # If it's not the green background
                        # This is a drawn line, keep it as black
                        painter.setPen(QPen(QColor(pixel_color)))
                        painter.drawPoint(x, y)

            painter.end()

            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=final_drawing,
                player_name=self.player_name,
                level="Level 1",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )
            print(f"Session saved successfully with metrics: {metrics}")
        except Exception as e:
            print(f"Error saving session: {e}")

    def show_popup_with_home(self):
        """Show completion popup with home button."""
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;          
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        """Return to home screen from popup."""
        popup.accept()
        self.open_main_screen()

    def paintEvent(self, event):
        """Paint the drawing and reference layers."""
        painter = QPainter(self)
        # Draw the current drawing (with green background during gameplay)
        painter.drawPixmap(0, 0, self.drawing)
        painter.drawPixmap(0, 0, self.reference_layer)

    def resizeEvent(self, event):
        """Handle window resize by recreating pixmaps."""
        new_drawing = QPixmap(self.size())
        new_drawing.fill(Qt.darkGreen)  # Keep green background during drawing
        QPainter(new_drawing).drawPixmap(0, 0, self.drawing)
        self.drawing = new_drawing

        new_reference = QPixmap(self.size())
        new_reference.fill(Qt.transparent)
        QPainter(new_reference).drawPixmap(0, 0, self.reference_layer)
        self.reference_layer = new_reference

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        timestamp = time.time()
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp

        if event.button() == Qt.LeftButton:
            if self.is_in_drawing_area(event.pos()):
                if self.last_pen_up_time is not None:
                    self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

                self.last_point = event.pos()
                self.last_time = timestamp
            else:
                self.last_point = None

    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if event.buttons() & Qt.LeftButton and self.last_point:
            timestamp = time.time()

            painter = QPainter(self.drawing)
            # Draw in cyan on green background during gameplay
            pen = QPen(Qt.cyan, 10, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(0)  # Mouse has no pressure

            delta_time = timestamp - self.last_time
            self.paper_time += delta_time
            self.last_time = timestamp

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        self.last_point = None
        self.last_pen_up_time = time.time()

    def tabletEvent(self, event: QTabletEvent):
        """Handle tablet events for pressure-sensitive drawing."""
        timestamp = time.time()
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp

        if event.type() == QTabletEvent.TabletPress:
            if self.is_in_drawing_area(event.pos()):
                if self.last_pen_up_time is not None:
                    self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

                self.last_point = event.pos()
                self.last_time = timestamp
                self.pendown_count += 1
            else:
                self.last_point = None

        elif event.type() == QTabletEvent.TabletMove and self.last_point is not None:
            painter = QPainter(self.drawing)
            pressure = event.pressure()
            # Draw in cyan on green background during gameplay
            pen = QPen(Qt.cyan, pressure * 50, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(pressure)

            delta_time = timestamp - self.last_time
            self.paper_time += delta_time
            self.last_time = timestamp

        elif event.type() == QTabletEvent.TabletRelease:
            self.last_point = None
            self.last_time = timestamp
            self.last_pen_up_time = timestamp

        event.accept()

    def open_main_screen(self):
        """Open the main screen."""
        self.hide()
        self.main_dialog.show()

class Level2_Screen(QWidget):
    def __init__(self, main_dialog, player_name, cursor_pixmap):
        super().__init__()
        self.player_name = player_name
        self.main_dialog = main_dialog
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.setWindowTitle("Level 2")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)

        # Set the selected cursor (scaled for gameplay)
        cursor_for_game = cursor_pixmap.scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setCursor(QCursor(cursor_for_game))

        self.reference_layer = QPixmap(self.size())  # Wave layer
        self.reference_layer.fill(Qt.transparent)

        # Start with green background during drawing
        self.drawing = QPixmap(self.size())  # User layer
        self.drawing.fill(Qt.darkGreen)

        self.last_point = None
        self.last_time = None

        # Timing variables
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.last_pen_up_time = None  # Track when pen was last lifted

        # Data collection variables
        self.pressure_readings = []
        self.pen_positions = []
        self.pen_timestamps = []
        self.pendown_count = 0

        self._setup_ui()
        self.draw_sin_wave()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.handle_next)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.label = QLabel(f"Level 2 - Welcome {self.player_name}")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def is_in_drawing_area(self, pos):
        """Returns True if pos is NOT inside the Next button rect."""
        btn_rect = self.next_btn.geometry()
        return not btn_rect.contains(pos)

    def draw_sin_wave(self):
        """Draw the reference sine wave."""
        painter = QPainter(self.reference_layer)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        amplitude = height // 7
        mid_y = height // 2

        prev_point = (0, mid_y)
        for x in range(1, width):
            y = mid_y - int(math.sin(x * 0.015) * amplitude)
            curr_point = (x, y)
            painter.drawLine(prev_point[0], prev_point[1], curr_point[0], curr_point[1])
            prev_point = curr_point

    def handle_next(self):
        """Handle next button click."""
        self.end_time = time.time()
        self.save_image_and_log()
        self.show_popup_with_home()

    def save_image_and_log(self):
        """Save the drawing and log all metrics using the metrics logger."""
        try:
            # Create a copy of the drawing with white background for final processing
            final_drawing = QPixmap(self.drawing.size())
            final_drawing.fill(Qt.white)  # White background for final image

            # Create a painter to copy only the drawn lines (not the background)
            painter = QPainter(final_drawing)

            # Create a mask to identify the drawn areas (non-green pixels)
            temp_image = self.drawing.toImage()
            green_color = QColor(Qt.darkGreen).rgb()

            # Paint the drawing onto white background, converting green to white
            for y in range(temp_image.height()):
                for x in range(temp_image.width()):
                    pixel_color = temp_image.pixel(x, y)
                    if pixel_color != green_color:  # If it's not the green background
                        # This is a drawn line, keep it as black
                        painter.setPen(QPen(QColor(pixel_color)))
                        painter.drawPoint(x, y)

            painter.end()

            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=final_drawing,
                player_name=self.player_name,
                level="Level 2",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )
            print(f"Session saved successfully with metrics: {metrics}")
        except Exception as e:
            print(f"Error saving session: {e}")

    def show_popup_with_home(self):
        """Show completion popup with home button."""
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;          
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        """Return to home screen from popup."""
        popup.accept()
        self.open_main_screen()

    def paintEvent(self, event):
        """Paint the drawing and reference layers."""
        painter = QPainter(self)
        # Draw the current drawing (with green background during gameplay)
        painter.drawPixmap(0, 0, self.drawing)
        painter.drawPixmap(0, 0, self.reference_layer)

    def resizeEvent(self, event):
        """Handle window resize by recreating pixmaps."""
        new_drawing = QPixmap(self.size())
        new_drawing.fill(Qt.darkGreen)  # Keep green background during drawing
        QPainter(new_drawing).drawPixmap(0, 0, self.drawing)
        self.drawing = new_drawing

        new_reference = QPixmap(self.size())
        new_reference.fill(Qt.transparent)
        QPainter(new_reference).drawPixmap(0, 0, self.reference_layer)
        self.reference_layer = new_reference

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        timestamp = time.time()
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp

        if event.button() == Qt.LeftButton:
            if self.is_in_drawing_area(event.pos()):
                if self.last_pen_up_time is not None:
                    self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

                self.last_point = event.pos()
                self.last_time = timestamp
            else:
                self.last_point = None

    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if event.buttons() & Qt.LeftButton and self.last_point:
            timestamp = time.time()

            painter = QPainter(self.drawing)
            # Draw in cyan on green background during gameplay
            pen = QPen(Qt.cyan, 10, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(0)  # Mouse has no pressure

            delta_time = timestamp - self.last_time
            self.paper_time += delta_time
            self.last_time = timestamp

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        self.last_point = None
        self.last_pen_up_time = time.time()

    def tabletEvent(self, event: QTabletEvent):
        """Handle tablet events for pressure-sensitive drawing."""
        timestamp = time.time()
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp

        if event.type() == QTabletEvent.TabletPress:
            if self.is_in_drawing_area(event.pos()):
                if self.last_pen_up_time is not None:
                    self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

                self.last_point = event.pos()
                self.last_time = timestamp
                self.pendown_count += 1
            else:
                self.last_point = None

        elif event.type() == QTabletEvent.TabletMove and self.last_point is not None:
            painter = QPainter(self.drawing)
            pressure = event.pressure()
            # Draw in cyan on green background during gameplay
            pen = QPen(Qt.cyan, pressure * 50, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(pressure)

            delta_time = timestamp - self.last_time
            self.paper_time += delta_time
            self.last_time = timestamp

        elif event.type() == QTabletEvent.TabletRelease:
            self.last_point = None
            self.last_time = timestamp
            self.last_pen_up_time = timestamp

        event.accept()

    def open_main_screen(self):
        """Open the main screen."""
        self.hide()
        self.main_dialog.show()


class Level3_Screen(QWidget):
    def __init__(self, main_dialog, player_name):
        super().__init__()
        self.setWindowTitle("Level 3 Cake Decorator")
        self.setFixedSize(2000, 1100)

        self.main_dialog = main_dialog
        self.player_name = player_name
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger with proper parameters
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.last_point = None
        self.last_time = None

        # Timing variables
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.last_pen_up_time = None  # Track when pen was last lifted

        # Data collection variables
        self.pressure_readings = []
        self.pen_positions = []
        self.pen_timestamps = []
        self.pendown_count = 0

        # Cake properties
        self.cake_x, self.cake_y = 150, 310
        self.cake_width, self.cake_height = 1700, 700
        self.rotation_angle = 0
        self.drawing_strokes = []
        self.current_stroke = []
        self.is_drawing = False

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)  # Add top margin
        self.setLayout(layout)

        self.label = QLabel(f"Hey {self.player_name}, follow the line and decorate the cake")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: black; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.setGeometry(1750, 950, 300, 150)
        self.next_btn.setStyleSheet(
            "color: black; border: none; border-radius: 30px; font-weight: bold; font-size: 50px;")
        self.next_btn.clicked.connect(self.handle_next)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(230, 240, 255))

        painter.save()
        painter.translate(self.cake_x + self.cake_width // 2, self.cake_y + self.cake_height // 2)
        painter.rotate(self.rotation_angle)
        painter.translate(-self.cake_width // 2, -self.cake_height // 2)

        self.draw_cake_base(painter)
        self.draw_candles(painter)
        self.draw_sine_wave_guide(painter)
        self.draw_user_drawings(painter)

        painter.restore()

    def draw_cake_base(self, painter):
        cake_color = QColor(139, 69, 19)
        painter.setBrush(QBrush(cake_color))
        painter.setPen(QPen(QColor(100, 50, 0), 2))
        cake_rect = QRectF(0, 5, self.cake_width, self.cake_height)
        painter.drawRoundedRect(cake_rect, 20, 20)

        painter.setBrush(QBrush(QColor(100, 50, 0)))
        painter.drawRoundedRect(QRectF(5, 10, self.cake_width - 10, self.cake_height - 10), 15, 15)

        painter.setBrush(QBrush(QColor(160, 82, 45)))
        painter.drawRoundedRect(QRectF(10, 15, self.cake_width - 20, self.cake_height - 20), 10, 10)

        painter.setBrush(QBrush(QColor(235, 169, 228)))
        painter.drawRoundedRect(QRectF(0, 0, self.cake_width, self.cake_height - 500), 20, 20)

        painter.setBrush(QBrush(QColor(125, 125, 125)))
        painter.drawRoundedRect(QRectF(-100, 700, 1900, 40), 20, 20)

    def draw_candles(self, painter):
        candle_count, candle_width, candle_height = 6, 50, 100
        candle_spacing = self.cake_width // (candle_count + 1)

        for i in range(candle_count):
            candle_x = candle_spacing * (i + 1) - candle_width // 2
            candle_y = -candle_height
            painter.setBrush(QBrush(QColor(241, 219, 13)))
            painter.setPen(QPen(QColor(200, 200, 100), 1))
            painter.drawRect(QRectF(candle_x, candle_y, candle_width, candle_height))

            flame_x, flame_y = candle_x + candle_width // 2, candle_y - 17
            flame_color = QColor(241, 124, 13)
            painter.setBrush(QBrush(flame_color))
            painter.setPen(QPen(QColor(255, 100, 0), 1))
            flame_points = [
                QPoint(flame_x, flame_y - 20), QPoint(flame_x + 8, flame_y + 10),
                QPoint(flame_x + 6, flame_y + 17), QPoint(flame_x, flame_y + 20),
                QPoint(flame_x - 6, flame_y + 17), QPoint(flame_x - 8, flame_y + 10),
            ]
            painter.drawPolygon(QPolygon(flame_points))

    def draw_sine_wave_guide(self, painter):
        painter.setPen(QPen(QColor(255, 255, 255, 200), 6, Qt.DashLine))
        wave_amplitude, wave_frequency, y_center = 110, 5.5, self.cake_height // 2
        step = 20
        points = []
        for x in range(20, self.cake_width - 10, step):
            progress = (x - 20) / (self.cake_width - 10)
            angle = progress * wave_frequency * -2 * math.pi
            y = y_center + wave_amplitude * math.sin(angle)
            points.append(QPoint(x, int(y)))
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

    def draw_user_drawings(self, painter):
        painter.setPen(QPen(QColor(13, 190, 241), 30, Qt.SolidLine, Qt.RoundCap))
        for stroke in self.drawing_strokes:
            for i in range(len(stroke) - 1):
                painter.drawLine(stroke[i], stroke[i + 1])
        for i in range(len(self.current_stroke) - 1):
            painter.drawLine(self.current_stroke[i], self.current_stroke[i + 1])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            cake_point = self.screen_to_cake_coords(event.pos())
            if cake_point and self.point_in_cake(cake_point):
                current_time = time.time()

                # Initialize start time if first touch
                if self.start_time is None:
                    self.start_time = current_time

                # Calculate air time if pen was up
                if self.last_pen_up_time is not None:
                    self.air_time += current_time - self.last_pen_up_time
                    self.last_pen_up_time = None

                self.is_drawing = True
                self.pendown_count += 1
                self.current_stroke = [cake_point]
                self.last_point = cake_point
                self.last_time = current_time

                # Record pen data
                self.pen_positions.append((cake_point.x(), cake_point.y()))
                self.pen_timestamps.append(current_time)
                # Simulate pressure (could be replaced with actual pressure data)
                self.pressure_readings.append(max(0.1, min(1.0, 0.5 + np.random.normal(0, 0.1))))

                event.accept()

    def mouseMoveEvent(self, event):
        if self.is_drawing and event.buttons() & Qt.LeftButton:
            cake_point = self.screen_to_cake_coords(event.pos())
            if cake_point and self.point_in_cake(cake_point):
                current_time = time.time()
                self.current_stroke.append(cake_point)

                # Calculate paper time since last point
                if self.last_time is not None:
                    self.paper_time += current_time - self.last_time

                # Record pen data
                self.pen_positions.append((cake_point.x(), cake_point.y()))
                self.pen_timestamps.append(current_time)
                # Simulate pressure variation during drawing
                self.pressure_readings.append(max(0.1, min(1.0, 0.5 + np.random.normal(0, 0.1))))

                self.last_point = cake_point
                self.last_time = current_time

                self.update()
                event.accept()

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            current_time = time.time()

            # Add final paper time from last point to release
            if self.last_time is not None:
                self.paper_time += current_time - self.last_time

            # Save current stroke and reset
            if self.current_stroke:
                self.drawing_strokes.append(self.current_stroke.copy())
            self.current_stroke.clear()

            self.is_drawing = False
            self.last_pen_up_time = current_time

            event.accept()

    def screen_to_cake_coords(self, screen_point):
        center_x, center_y = self.cake_x + self.cake_width // 2, self.cake_y + self.cake_height // 2
        rel_x, rel_y = screen_point.x() - center_x, screen_point.y() - center_y
        angle_rad = math.radians(-self.rotation_angle)
        rotated_x = rel_x * math.cos(angle_rad) - rel_y * math.sin(angle_rad)
        rotated_y = rel_x * math.sin(angle_rad) + rel_y * math.cos(angle_rad)
        return QPoint(int(rotated_x + self.cake_width // 2), int(rotated_y + self.cake_height // 2))

    def point_in_cake(self, point):
        margin = 10
        return (margin <= point.x() <= self.cake_width - margin and
                margin <= point.y() <= self.cake_height - margin)

    def handle_next(self):
        # Set end time and finalize air time
        self.end_time = time.time()
        if self.last_pen_up_time is not None:
            self.air_time += self.end_time - self.last_pen_up_time

        self.save_image_and_log()
        self.show_popup_with_home()

    def create_drawing_pixmap(self):
        """Create a QPixmap of the current drawing for the metrics logger"""
        # Create a pixmap to draw on
        pixmap = QPixmap(self.cake_width, self.cake_height)
        pixmap.fill(Qt.white)  # Fill with white background

        # Create painter for the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the user's strokes
        painter.setPen(QPen(QColor(0, 0, 0), 30, Qt.SolidLine, Qt.RoundCap))  # Black strokes
        for stroke in self.drawing_strokes:
            for i in range(len(stroke) - 1):
                painter.drawLine(stroke[i], stroke[i + 1])

        painter.end()
        return pixmap

    def save_image_and_log(self):
        """Save drawing image and log all metrics to Excel using DrawingMetricsLogger"""
        try:
            # Create drawing pixmap
            drawing_pixmap = self.create_drawing_pixmap()

            # Use the complete session method from DrawingMetricsLogger
            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=drawing_pixmap,
                player_name=self.player_name,
                level="Level 3",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )

        except Exception as e:
            print(f"Error saving data: {e}")
            import traceback
            traceback.print_exc()

    def show_popup_with_home(self):
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)
        layout = QVBoxLayout()

        label = QLabel("Good Job!", popup)
        label.setStyleSheet("font-size: 70px; font-weight: bold; color: black;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        home_btn = QPushButton("Home", popup)
        home_btn.setFixedSize(300, 100)
        home_btn.setStyleSheet("font-size: 40px; background-color: lightblue;")
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        popup.accept()
        self.open_main_screen()

    def open_main_screen(self):
        self.hide()
        self.main_dialog.show()


class Level4_Screen(QWidget):
    def __init__(self, main_dialog, player_name, cursor_pixmap):
        super().__init__()
        self.setWindowTitle("Level 4 - Wolfs Chase")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)

        self.main_dialog = main_dialog
        self.player_name = player_name
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger with proper parameters
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        # Initialize tracking variables
        self.last_point = None
        self.last_time = None

        # Timing variables
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.last_pen_up_time = None

        # Data collection variables
        self.pressure_readings = []
        self.pen_positions = []
        self.pen_timestamps = []
        self.pendown_count = 0
        self.drawing_strokes = []
        self.current_stroke = []
        self.is_drawing = False

        # Set up layout
        self.layout = QVBoxLayout()
        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Arial", 16))
        home_btn.setFixedWidth(200)
        home_btn.clicked.connect(self.open_main_screen)
        self.layout.addWidget(home_btn, alignment=Qt.AlignLeft)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.save_image_and_log)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
                  QPushButton {
                      color: white;
                      border: none;
                      border-radius: 30px;
                      font-weight: bold;
                      font-size: 50px;
                  }
              """)
        # Store the next button's geometry for drawing exclusion
        self.next_btn_rect = self.next_btn.geometry()

        self.label = QLabel(f"Hi {self.player_name}, get ready to run from the wolf")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: white;")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addStretch()
        self.setLayout(self.layout)

        # Set custom cursor
        cursor_for_game = cursor_pixmap.scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setCursor(QCursor(cursor_for_game))

        # Canvas for drawing
        self.drawing = QPixmap(2000, 1100)
        self.drawing.fill(Qt.darkGreen)

        # Trail image
        self.trail_img = QPixmap("wolf.png")
        if self.trail_img.isNull():
            print("ERROR: Could not load wolf.png from", os.getcwd())
            self.trail_img = QPixmap(100, 100)
            self.trail_img.fill(Qt.red)

        self.trail_img = self.trail_img.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.trail_pos = QPoint(-100, -100)
        self.cursor_pos = QPoint(-100, -100)

        # Trail distance variables
        self.initial_trail_distance = 250
        self.final_trail_distance = 70
        self.current_trail_distance = self.initial_trail_distance

        # Start the trail movement timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_trail)
        self.timer.start(16)

        # Draw spiral AFTER shown
        QTimer.singleShot(0, self.draw_spiral)

    def draw_spiral(self):
        painter = QPainter(self.drawing)
        pen = QPen(Qt.black, 10)
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = 700
        a = 0
        b = 25
        theta = 0
        max_theta = 6 * math.pi
        step = 0.1

        prev_x, prev_y = center_x, center_y
        while theta < max_theta:
            r = a + b * theta
            x = center_x + int(r * math.cos(theta))
            y = center_y + int(r * math.sin(theta))
            painter.drawLine(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y
            theta += step
        self.update()

    def is_over_next_button(self, pos):
        """Check if the given position is over the next button."""
        # Update button rect in case window was resized
        self.next_btn_rect = self.next_btn.geometry()
        return self.next_btn_rect.contains(pos)
        """Create a version of the drawing with white background and crop y-axis for saving."""
        if self.drawing is None:
            return QPixmap(self.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.drawing)

        # Draw trailing image
        trail_draw_pos = self.trail_pos - QPoint(self.trail_img.width() // 2, self.trail_img.height() // 2)
        painter.drawPixmap(trail_draw_pos, self.trail_img)

    def resizeEvent(self, event):
        new_pixmap = QPixmap(self.size())
        new_pixmap.fill(Qt.darkGreen)
        painter = QPainter(new_pixmap)
        painter.drawPixmap(0, 0, self.drawing)
        self.drawing = new_pixmap

    def mousePressEvent(self, event):
        # Check if clicking on the next button area - if so, don't start drawing
        if self.is_over_next_button(event.pos()):
            return

        if event.button() == Qt.LeftButton:
            current_time = time.time()

            # Initialize start time if first touch
            if self.start_time is None:
                self.start_time = current_time

            # Calculate air time if pen was up
            if self.last_pen_up_time is not None:
                self.air_time += current_time - self.last_pen_up_time
                self.last_pen_up_time = None

            self.is_drawing = True
            self.current_stroke = [event.pos()]
            self.last_point = event.pos()
            self.last_time = current_time

            # Record pen data
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            # Simulate pressure (could be replaced with actual pressure data)
            self.pressure_readings.append(max(0.1, min(1.0, 0.5 + np.random.normal(0, 0.1))))

    def mouseMoveEvent(self, event):
        # Don't draw if we're over the next button
        if self.is_over_next_button(event.pos()):
            return

        self.cursor_pos = event.pos()

        if self.is_drawing and event.buttons() & Qt.LeftButton and self.last_point:
            current_time = time.time()

            # Draw the line
            painter = QPainter(self.drawing)
            pen = QPen(Qt.darkMagenta, 15, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())

            # Add to current stroke
            self.current_stroke.append(event.pos())

            # Calculate paper time since last point
            if self.last_time is not None:
                self.paper_time += current_time - self.last_time

            # Record pen data
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            # Simulate pressure variation during drawing
            self.pressure_readings.append(max(0.1, min(1.0, 0.5 + np.random.normal(0, 0.1))))

            self.last_point = event.pos()
            self.last_time = current_time
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            current_time = time.time()

            # Add final paper time from last point to release
            if self.last_time is not None:
                self.paper_time += current_time - self.last_time

            # Save current stroke and reset
            if self.current_stroke:
                self.drawing_strokes.append(self.current_stroke.copy())
            self.current_stroke.clear()

            self.is_drawing = False
            self.last_pen_up_time = current_time
            self.last_point = None

    def tabletEvent(self, event: QTabletEvent):
        # Check if over the next button area - if so, don't draw
        if self.is_over_next_button(event.pos()):
            return

        if event.type() == QTabletEvent.TabletPress:
            current_time = time.time()

            # Initialize start time if first touch
            if self.start_time is None:
                self.start_time = current_time

            # Calculate air time if pen was up
            if self.last_pen_up_time is not None:
                self.air_time += current_time - self.last_pen_up_time
                self.last_pen_up_time = None

            self.is_drawing = True
            self.pendown_count += 1
            self.current_stroke = [event.pos()]
            self.last_point = event.pos()
            self.last_time = current_time

            # Record pen data with actual pressure
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            self.pressure_readings.append(max(0.1, min(1.0, event.pressure())))

        elif event.type() == QTabletEvent.TabletMove and self.is_drawing and self.last_point:
            current_time = time.time()

            # Draw the line
            painter = QPainter(self.drawing)
            pen = QPen(Qt.darkMagenta, event.pressure() * 50, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())

            # Add to current stroke
            self.current_stroke.append(event.pos())

            # Calculate paper time since last point
            if self.last_time is not None:
                self.paper_time += current_time - self.last_time

            # Record pen data with actual pressure
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            self.pressure_readings.append(max(0.1, min(1.0, event.pressure())))

            self.last_point = event.pos()
            self.last_time = current_time
            self.update()

        elif event.type() == QTabletEvent.TabletRelease:
            if self.is_drawing:
                current_time = time.time()

                # Add final paper time from last point to release
                if self.last_time is not None:
                    self.paper_time += current_time - self.last_time

                # Save current stroke and reset
                if self.current_stroke:
                    self.drawing_strokes.append(self.current_stroke.copy())
                self.current_stroke.clear()

                self.is_drawing = False
                self.last_pen_up_time = current_time
                self.last_point = None

        event.accept()

    def update_trail(self):
        # Calculate progress based on drawing activity (paper time)
        if self.start_time is not None:
            # Use a reasonable duration for full transition (e.g., 30 seconds)
            transition_duration = 10.0
            elapsed_time = time.time() - self.start_time
            progress = min(1.0, elapsed_time / transition_duration)

            # Interpolate distance from 400 to 100 pixels
            self.current_trail_distance = self.initial_trail_distance - (
                        self.initial_trail_distance - self.final_trail_distance) * progress

        # Calculate direction from trail to cursor
        dx = self.cursor_pos.x() - self.trail_pos.x()
        dy = self.cursor_pos.y() - self.trail_pos.y()

        # Calculate current distance
        current_distance = (dx * dx + dy * dy) ** 0.5

        # If we're too close or too far, adjust accordingly
        if current_distance > 0:
            # Calculate target position based on desired trail distance
            target_distance = self.current_trail_distance

            # Normalize direction vector
            unit_dx = dx / current_distance
            unit_dy = dy / current_distance

            # Calculate target position (trail_distance pixels behind cursor)
            target_x = self.cursor_pos.x() - unit_dx * target_distance
            target_y = self.cursor_pos.y() - unit_dy * target_distance

            # Move trail towards target position with smooth interpolation
            trail_speed = 0.1
            self.trail_pos += QPoint(
                int((target_x - self.trail_pos.x()) * trail_speed),
                int((target_y - self.trail_pos.y()) * trail_speed)
            )

        self.update()

    def create_drawing_pixmap(self):
        """Create a clean QPixmap of just the user's drawing for the metrics logger"""
        # Create a pixmap with white background for the drawing strokes only
        pixmap = QPixmap(self.drawing.size())
        pixmap.fill(Qt.white)

        # Create painter for the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the user's strokes in black
        painter.setPen(QPen(Qt.black, 15, Qt.SolidLine, Qt.RoundCap))
        for stroke in self.drawing_strokes:
            for i in range(len(stroke) - 1):
                painter.drawLine(stroke[i], stroke[i + 1])

        painter.end()
        return pixmap

    def save_image_and_log(self):
        """Save drawing image and log all metrics to Excel using DrawingMetricsLogger"""
        # Set end time and finalize air time
        self.end_time = time.time()
        if self.last_pen_up_time is not None:
            self.air_time += self.end_time - self.last_pen_up_time

        try:
            # Create drawing pixmap (clean version with just user strokes)
            drawing_pixmap = self.create_drawing_pixmap()

            # Use the complete session method from DrawingMetricsLogger
            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=drawing_pixmap,
                player_name=self.player_name,
                level="Level 4",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )

            print(f"Successfully saved metrics for {self.player_name} - Level 4")

            # Show completion message or navigate to next screen
            self.show_popup_with_home()

        except Exception as e:
            print(f"Error saving data: {e}")
            import traceback
            traceback.print_exc()

    def show_popup_with_home(self):
        """Show a custom popup with home button"""
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        """Close popup and return to main screen"""
        popup.close()
        self.open_main_screen()

    def open_main_screen(self):
        self.hide()
        self.main_dialog.show()

class Level5_Screen(QWidget):

    def __init__(self, main_dialog, player_name):
        super().__init__()

        self.setWindowTitle("Level 5 - Snail Shell")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger with proper parameters
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.main_dialog = main_dialog
        self.player_name = player_name
        self.last_point = None
        self.last_pen_up_time = None
        self.last_time = None

        # Drawing metrics tracking
        self.pen_positions = []
        self.pen_timestamps = []
        self.pressure_readings = []
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.pendown_count = 0
        self.is_drawing = False
        self.air_start_time = None
        self.paper_start_time = None

        # Load background image
        self.original_bg_pixmap = QPixmap("snail_back1.png")
        if self.original_bg_pixmap.isNull():
            print("Error: Could not load snail_back1.png")
            return

        # Set up layout
        self.layout = QVBoxLayout()
        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Arial", 16))
        home_btn.setFixedWidth(200)
        home_btn.clicked.connect(self.open_main_screen)
        self.layout.addWidget(home_btn, alignment=Qt.AlignLeft)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.handle_next)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.label = QLabel(f"Hey {self.player_name}, draw the spirals in the snail")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: black;")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addStretch()
        self.setLayout(self.layout)

        # Initialize drawing session
        self.start_time = time.time()
        self.air_start_time = self.start_time

    def showEvent(self, event):
        super().showEvent(event)

        # Reinitialize drawing layers now that the widget has a valid size
        self.drawing = QPixmap(self.size())
        self.drawing.fill(Qt.transparent)

        self.reference_layer = QPixmap(self.size())
        self.reference_layer.fill(Qt.transparent)

        self.draw_spiral()

    def draw_spiral(self):
        if self.reference_layer.isNull():
            return

        painter = QPainter(self.reference_layer)
        pen = QPen(Qt.black, 10)
        painter.setPen(pen)

        center_x = 1125
        center_y = 600
        a = 0
        b = 23
        theta = 0
        max_theta = 6 * math.pi
        step = 0.1

        prev_x, prev_y = center_x, center_y
        while theta < max_theta:
            r = a + b * theta
            x = center_x + int(r * math.cos(theta))
            y = center_y + int(r * math.sin(theta))
            painter.drawLine(prev_x, prev_y, x, y)
            prev_x, prev_y = x, y
            theta += step

        # End the painter properly
        painter.end()
        self.update()

    def create_white_background_drawing(self):
        """Create a version of the drawing with white background for saving."""
        # Create a new pixmap with white background
        white_drawing = QPixmap(self.drawing.size())
        white_drawing.fill(Qt.white)

        # Paint the drawing content on top of the white background
        painter = QPainter(white_drawing)
        painter.drawPixmap(0, 0, self.drawing)
        painter.end()

        return white_drawing

    def handle_next(self):
        # Ensure end time is recorded
        if self.end_time is None:
            self.end_time = time.time()

        # If we're currently in air time, add the final air time
        if self.last_pen_up_time is not None:
            self.air_time += (self.end_time - self.last_pen_up_time)

        # Check if there's any drawing content before saving
        if self.has_drawing_content():
            self.save_image_and_log()
        else:
            print("No drawing content detected. Skipping image processing.")
            # Still save basic metrics even without drawing
            self.save_basic_metrics()

        self.show_popup_with_home()

    def has_drawing_content(self):
        """Check if the drawing pixmap has any non-transparent content."""
        # Convert pixmap to image to check for content
        temp_path = "temp_check.png"
        self.drawing.save(temp_path)

        try:
            from PIL import Image
            import numpy as np

            # Load image and check if it has any non-transparent pixels
            img = Image.open(temp_path).convert("RGBA")
            img_array = np.array(img)

            # Check alpha channel - if all pixels are transparent (alpha = 0), no content
            has_content = np.any(img_array[:, :, 3] > 0)

            # Clean up temp file
            os.remove(temp_path)
            return has_content

        except Exception as e:
            print(f"Error checking drawing content: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
            # Default to True to avoid skipping legitimate drawings
            return True

    def save_basic_metrics(self):
        """Save basic metrics without image processing when no drawing exists."""
        if self.metrics_logger is None:
            print("Warning: metrics_logger is None. Skipping logging.")
            return

        try:
            # Ensure we have valid start and end times
            if self.start_time is None:
                self.start_time = time.time()
            if self.end_time is None:
                self.end_time = time.time()

            # Calculate basic metrics manually for empty drawing
            total_time = self.end_time - self.start_time if self.start_time else 0

            # Create a basic metrics dictionary - this won't be used by DrawingMetricsLogger
            # but kept for debugging/logging purposes
            basic_metrics = {
                'total_time': total_time,
                'air_time': self.air_time,
                'paper_time': self.paper_time,
                'mean_speed': 0,
                'mean_acceleration': 0,
                'mean_pressure': 0,
                'pressure_variance': 0,
                'pendown_count': self.pendown_count,
                'max_x': 0,
                'max_y': 0,
                'gmrtp': 0,
                'mean_jerk': 0,
                'avg_cisp': 0
            }

            print(f"Basic metrics calculated. Total time: {basic_metrics['total_time']:.2f}s, No drawing content.")

        except Exception as e:
            print(f"Error calculating basic metrics: {e}")

    def save_image_and_log(self):
        if self.metrics_logger is None:
            print("Warning: metrics_logger is None. Skipping logging.")
            return

        try:
            # Ensure we have valid start and end times
            if self.start_time is None:
                self.start_time = time.time()
            if self.end_time is None:
                self.end_time = time.time()

            # Only proceed if we have actual pen positions (drawing data)
            if not self.pen_positions:
                print("No pen position data available. Saving basic metrics only.")
                self.save_basic_metrics()
                return

            # Create white background version for the logger
            white_drawing = self.create_white_background_drawing()

            # Use the DrawingMetricsLogger's save_complete_session method
            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=white_drawing,  # Pass the white background version
                player_name=self.player_name,
                level="Level 5",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )
            print(f"Session saved successfully. Total time: {metrics['total_time']:.2f}s")
            return metrics
        except Exception as e:
            print(f"Error saving session: {e}")
            # Try to save basic metrics as fallback
            self.save_basic_metrics()
            return None

    def show_popup_with_home(self):
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        popup.accept()
        self.open_main_screen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(200, 150, self.original_bg_pixmap)
        painter.drawPixmap(0, 0, self.reference_layer)
        painter.drawPixmap(0, 0, self.drawing)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Resize and reinitialize the drawing pixmaps
        size = event.size()
        if size.width() > 0 and size.height() > 0:
            self.drawing = QPixmap(size)
            self.drawing.fill(Qt.transparent)

            self.reference_layer = QPixmap(size)
            self.reference_layer.fill(Qt.transparent)

            self.draw_spiral()

    def mousePressEvent(self, event):
        timestamp = time.time()

        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp
            self.air_start_time = timestamp

        if event.button() == Qt.LeftButton:
            if self.is_in_drawing_area(event.pos()):
                # Handle transition from air to paper
                if self.last_pen_up_time is not None:
                    self.air_time += (timestamp - self.last_pen_up_time)
                    self.last_pen_up_time = None

                # Start drawing
                self.is_drawing = True
                self.pendown_count += 1
                self.last_point = event.pos()
                self.paper_start_time = timestamp
                self.last_time = timestamp

                # Record the initial position
                self.pen_positions.append((event.pos().x(), event.pos().y()))
                self.pen_timestamps.append(timestamp)
                self.pressure_readings.append(1.0)  # Default pressure value
            else:
                self.last_point = None
                self.is_drawing = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_point and self.is_drawing:
            timestamp = time.time()

            # Draw the line
            painter = QPainter(self.drawing)
            pen = QPen(Qt.darkBlue, 40,Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()  # Properly end the painter

            self.last_point = event.pos()
            self.update()

            # Record metrics
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(1.0)  # Default pressure value

            # Update paper time
            if self.last_time is not None:
                delta_time = timestamp - self.last_time
                self.paper_time += delta_time
            self.last_time = timestamp

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.last_point = None
            self.last_pen_up_time = time.time()

    def is_in_drawing_area(self, pos):
        return 0 <= pos.x() < self.width() and 0 <= pos.y() < self.height()

    def open_main_screen(self):
        self.hide()
        self.main_dialog.show()

class Level6_Screen(QWidget):
    def __init__(self, main_dialog, player_name):
        super().__init__()

        self.setWindowTitle("Level 6 - Name Writing")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger with proper parameters
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.main_dialog = main_dialog
        self.player_name = player_name
        self.last_point = None
        self.last_pen_up_time = None
        self.last_time = None

        # Drawing metrics tracking
        self.pen_positions = []
        self.pen_timestamps = []
        self.pressure_readings = []
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.pendown_count = 0
        self.is_drawing = False
        self.air_start_time = None
        self.paper_start_time = None

        # Initialize drawing canvas
        self.drawing = None

        # Set up layout
        self.layout = QVBoxLayout()
        home_btn = QPushButton("Home")
        home_btn.setFont(QFont("Arial", 16))
        home_btn.setFixedWidth(200)
        home_btn.clicked.connect(self.open_main_screen)
        self.layout.addWidget(home_btn, alignment=Qt.AlignLeft)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.handle_next)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        # Store the next button's geometry for drawing exclusion
        self.next_btn_rect = self.next_btn.geometry()

        self.label = QLabel(f"Hey {self.player_name}, let's try writing your name")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: white;")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.layout.addStretch()
        self.setLayout(self.layout)

        # Initialize drawing session
        self.start_time = time.time()
        self.air_start_time = self.start_time

    def showEvent(self, event):
        super().showEvent(event)

        # Initialize drawing canvas with proper size
        self.drawing = QPixmap(self.size())
        self.drawing.fill(Qt.darkCyan)

        # Draw the player's name as reference
        self.draw_reference_name()

    def draw_reference_name(self):
        """Draw the player's name as reference text."""
        if self.drawing is None:
            return

        painter = QPainter(self.drawing)
        font = QFont("Lucida Handwriting", 100, QFont.Bold)
        font.setStyleStrategy(QFont.PreferAntialias)
        painter.setFont(font)
        painter.setPen(QPen(Qt.black, 3))

        # Calculate text size to center it
        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(self.player_name)
        text_height = metrics.height()

        x = (self.width() - text_width) // 2
        y = (self.height() + text_height) // 2

        painter.drawText(x, y, self.player_name)
        painter.end()

    def is_over_next_button(self, pos):
        """Check if the given position is over the next button."""
        # Update button rect in case window was resized
        self.next_btn_rect = self.next_btn.geometry()
        return self.next_btn_rect.contains(pos)
        """Create a version of the drawing with white background and crop y-axis for saving."""
        if self.drawing is None:
            return QPixmap(self.size())

        # Calculate cropped dimensions
        original_height = self.drawing.height()
        original_width = self.drawing.width()
        crop_top = 300
        crop_bottom = 250

        # Ensure we don't crop more than the image height
        if crop_top + crop_bottom >= original_height:
            crop_top = 0
            crop_bottom = 0

        cropped_height = original_height - crop_top - crop_bottom

        # Create a new pixmap with white background and cropped size
        white_drawing = QPixmap(original_width, cropped_height)
        white_drawing.fill(Qt.white)

        # Paint the cropped portion of the original drawing
        painter = QPainter(white_drawing)
        # Draw only the cropped portion (remove 200px from top, 50px from bottom)
        painter.drawPixmap(0, 0, self.drawing, 0, crop_top, original_width, cropped_height)
        painter.end()

        return white_drawing

    def handle_next(self):
        """Handle next button click."""
        # Ensure end time is recorded
        if self.end_time is None:
            self.end_time = time.time()

        # If we're currently in air time, add the final air time
        if self.last_pen_up_time is not None:
            self.air_time += (self.end_time - self.last_pen_up_time)

        # Check if there's any drawing content before saving
        if self.has_drawing_content():
            self.save_image_and_log()
        else:
            print("No drawing content detected. Skipping image processing.")
            # Still save basic metrics even without drawing
            self.save_basic_metrics()

        self.show_popup_with_home()

    def has_drawing_content(self):
        """Check if there's actual user drawing content beyond the reference text."""
        # Since we have user drawing on top of reference text, check if pen positions exist
        return len(self.pen_positions) > 0

    def save_basic_metrics(self):
        """Save basic metrics without image processing when no drawing exists."""
        if self.metrics_logger is None:
            print("Warning: metrics_logger is None. Skipping logging.")
            return

        try:
            # Ensure we have valid start and end times
            if self.start_time is None:
                self.start_time = time.time()
            if self.end_time is None:
                self.end_time = time.time()

            # Calculate basic metrics manually for empty drawing
            total_time = self.end_time - self.start_time if self.start_time else 0

            print(f"Basic metrics calculated. Total time: {total_time:.2f}s, No drawing content.")

        except Exception as e:
            print(f"Error calculating basic metrics: {e}")
    def create_white_background_drawing(self):
        """Create a version of the drawing with white background for saving."""
        # Create a new pixmap with white background
        white_drawing = QPixmap(self.drawing.size())
        white_drawing.fill(Qt.white)

        # Paint the drawing content on top of the white background
        painter = QPainter(white_drawing)
        painter.drawPixmap(0, 0, self.drawing)
        painter.end()

        return white_drawing

    def save_image_and_log(self):
        """Save the drawing and log all metrics using the metrics logger."""
        if self.metrics_logger is None:
            print("Warning: metrics_logger is None. Skipping logging.")
            return

        if self.drawing is None:
            print("Warning: drawing is None. Skipping logging.")
            return

        try:
            # Ensure we have valid start and end times
            if self.start_time is None:
                self.start_time = time.time()
            if self.end_time is None:
                self.end_time = time.time()

            # Only proceed if we have actual pen positions (drawing data)
            if not self.pen_positions:
                print("No pen position data available. Saving basic metrics only.")
                self.save_basic_metrics()
                return

            # Create white background version for the logger
            white_drawing = self.create_white_background_drawing()

            # Use the DrawingMetricsLogger's save_complete_session method
            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=white_drawing,  # Pass the white background version
                player_name=self.player_name,
                level="Level 6",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )
            print(f"Session saved successfully. Total time: {metrics['total_time']:.2f}s")
            return metrics

        except Exception as e:
            print(f"Error saving session: {e}")
            # Try to save basic metrics as fallback
            self.save_basic_metrics()
            return None

    def show_popup_with_home(self):
        """Show completion popup with home button."""
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;          
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        popup.accept()
        self.open_main_screen()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Resize and reinitialize the drawing pixmap
        size = event.size()
        if size.width() > 0 and size.height() > 0:
            old_drawing = self.drawing
            self.drawing = QPixmap(size)
            self.drawing.fill(Qt.darkCyan)

            # Copy old content if it exists
            if old_drawing and not old_drawing.isNull():
                painter = QPainter(self.drawing)
                painter.drawPixmap(0, 0, old_drawing)
                painter.end()

            # Redraw reference name
            self.draw_reference_name()

    def paintEvent(self, event):
        if self.drawing is not None:
            base_painter = QPainter(self)
            base_painter.drawPixmap(0, 0, self.drawing)

    def mousePressEvent(self, event):
        # Check if clicking on the next button area - if so, don't start drawing
        if self.is_over_next_button(event.pos()):
            return

        timestamp = time.time()

        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp
            self.air_start_time = timestamp

        if event.button() == Qt.LeftButton:
            # Handle transition from air to paper
            if self.last_pen_up_time is not None:
                self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

            # Start drawing
            self.is_drawing = True
            self.last_point = event.pos()
            self.paper_start_time = timestamp
            self.last_time = timestamp

            # Record the initial position
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(0.5)  # Default pressure value for mouse

    def mouseMoveEvent(self, event):
        # Don't draw if we're over the next button
        if self.is_over_next_button(event.pos()):
            return

        if event.buttons() & Qt.LeftButton and self.last_point and self.is_drawing and self.drawing is not None:
            timestamp = time.time()

            # Draw the line
            painter = QPainter(self.drawing)
            pen = QPen(Qt.darkBlue, 40, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.last_point = event.pos()
            self.update()

            # Record metrics
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(0.5)  # Default pressure value for mouse

            # Update paper time
            if self.last_time is not None:
                delta_time = timestamp - self.last_time
                self.paper_time += delta_time
            self.last_time = timestamp

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.last_point = None
            self.last_pen_up_time = time.time()

    def tabletEvent(self, event: QTabletEvent):
        # Check if over the next button area - if so, don't draw
        if self.is_over_next_button(event.pos()):
            return

        timestamp = time.time()

        # Initialize start time if not set
        if self.start_time is None:
            self.start_time = timestamp
            self.last_time = timestamp
            self.air_start_time = timestamp

        if event.type() == QTabletEvent.TabletPress:
            # Handle transition from air to paper
            if self.last_pen_up_time is not None:
                self.air_time += (timestamp - self.last_pen_up_time)
                self.last_pen_up_time = None

            # Start drawing
            self.is_drawing = True
            self.pendown_count += 1
            self.last_point = event.pos()
            self.paper_start_time = timestamp
            self.last_time = timestamp

            # Record the initial position
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(event.pressure())

        elif event.type() == QTabletEvent.TabletMove and self.last_point and self.is_drawing and self.drawing is not None:
            # Draw the line
            painter = QPainter(self.drawing)
            pen = QPen(Qt.darkBlue, 40, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.last_point = event.pos()
            self.update()

            # Record metrics
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(timestamp)
            self.pressure_readings.append(event.pressure())

            # Update paper time
            if self.last_time is not None:
                delta_time = timestamp - self.last_time
                self.paper_time += delta_time
            self.last_time = timestamp

        elif event.type() == QTabletEvent.TabletRelease:
            if self.is_drawing:
                self.is_drawing = False
                self.last_point = None
                self.last_pen_up_time = time.time()

        event.accept()

    def open_main_screen(self):
        self.hide()
        self.main_dialog.show()

class Level7_Screen(QWidget):
    def __init__(self, main_dialog, player_name):
        super().__init__()
        self.main_dialog = main_dialog
        self.player_name = player_name
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        # Initialize the metrics logger with proper parameters
        self.metrics_logger = DrawingMetricsLogger(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.setWindowTitle("Level 7 - Puppy Name Drawing")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)

        # Drawing metrics tracking
        self.pen_positions = []
        self.pen_timestamps = []
        self.pressure_readings = []
        self.stroke_boundaries = []  # Track where each stroke starts/ends
        self.start_time = None
        self.end_time = None
        self.air_time = 0
        self.paper_time = 0
        self.pendown_count = 0
        self.is_drawing = False
        self.air_start_time = None
        self.paper_start_time = None
        self.session_saved = False  # Flag to prevent duplicate saving

        self.puppy_names = [
            "Falcon", "Jasper", "Magnus", "Poppy", "Teddy", "Biscuit", "Noodle",
            "Doodle", "Bandit", "Button", "Shadow", "Fuzzy", "Bubbles",
            "Sprinkle", "Cookie", "Tater Tot", "Waffles", "Peach", "Muffin",
            "Blossom", "Churro", "Fluffy", "Sunshine", "Honey", "Bailey",
            "Cupcake", "Daisy", "Chewy", "Pudding", "Pickles", "Wiggles",
            "Harley", "Gumdrop"
        ]

        self.current_puppy_name = ""  # Start with no name
        self.last_point = None

        # Puppy image at top
        self.bg1_label = QLabel(self)
        self.bg1_label.setScaledContents(True)
        pixmap = QPixmap("puppy.png")
        if not pixmap.isNull():
            self.bg1_label.setPixmap(pixmap)
            self.bg1_label.setGeometry(500, 100, 1000, 700)

        # Layout
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(200)
        home_btn.setFont(QFont("Arial", 16))
        home_btn.clicked.connect(self.open_main_screen)
        top_layout.addWidget(home_btn, alignment=Qt.AlignLeft)

        self.next_btn = QPushButton("Next", self)
        self.next_btn.clicked.connect(self.handle_next)
        self.next_btn.move(1750, 950)
        self.next_btn.resize(300, 150)
        self.next_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.name_btn = QPushButton("Puppy Names")
        self.name_btn.setFixedWidth(300)
        self.name_btn.setFont(QFont("Arial", 16))
        self.name_btn.clicked.connect(self.generate_new_name)
        top_layout.addWidget(self.name_btn, alignment=Qt.AlignRight)

        layout.addLayout(top_layout)

        self.label = QLabel(f"Hey {self.player_name}, Select and write the name for your Puppy")
        self.label.setFont(QFont("Arial", 28))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

        # Initialize drawing area
        self.drawing = QPixmap(self.size())
        self.drawing.fill(QColor(13, 190, 241))  # blue background

        # Initialize drawing session
        self.start_time = time.time()
        self.air_start_time = self.start_time

        self.draw_white_box()  # draw box initially

    def draw_white_box(self):
        painter = QPainter(self.drawing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Clear and draw background
        self.drawing.fill(QColor(13, 190, 241))

        # Box coordinates
        box_width = 1200
        box_height = 340
        box_x = (self.width() - box_width) // 2
        box_y = 705

        # White rectangle
        painter.setBrush(QBrush(Qt.white))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawRect(box_x, box_y, box_width, box_height)

        # Draw name (if any)
        if self.current_puppy_name:
            font = QFont("Lucida Handwriting", 80, QFont.Bold)
            font.setStyleStrategy(QFont.PreferAntialias)
            painter.setFont(font)
            painter.setPen(QPen(QColor(157, 13, 241), 2))
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(self.current_puppy_name)
            text_height = metrics.height()
            text_x = box_x + (box_width - text_width) // 2
            text_y = box_y + (box_height + text_height) // 2 - 40
            painter.drawText(text_x, text_y, self.current_puppy_name)

        painter.end()
        self.update()  # force repaint

    def handle_next(self):
        """Handle next button click."""
        self.pendown_count=self.pendown_count-1
        if not self.session_saved:
            self.save_image_and_log()
        self.show_popup_with_home()


    def save_image_and_log(self):
        """Save the drawing and log all metrics using the metrics logger."""
        if not self.metrics_logger or self.session_saved:
            return

        try:
            # Finalize timing metrics
            self.end_time = time.time()

            # Add any remaining air time
            if self.air_start_time and not self.is_drawing:
                self.air_time += self.end_time - self.air_start_time

            # Add any remaining paper time
            if self.paper_start_time and self.is_drawing:
                self.paper_time += self.end_time - self.paper_start_time


            # Create a final image with only the white box content
            final_drawing = self.create_final_image()

            metrics = self.metrics_logger.save_complete_session(
                drawing_pixmap=final_drawing,
                player_name=self.player_name,
                level="Level 7",
                pen_positions=self.pen_positions,
                pen_timestamps=self.pen_timestamps,
                pressure_readings=self.pressure_readings,
                start_time=self.start_time,
                end_time=self.end_time,
                air_time=self.air_time,
                paper_time=self.paper_time,
                pendown_count=self.pendown_count
            )
            print(f"Session saved successfully. Total time: {metrics['total_time']:.2f}s")
            self.session_saved = True  # Mark as saved

        except Exception as e:
            print(f"Error saving session: {e}")

    def create_final_image(self):
        """Create final image containing only the white box area with user drawing (no pre-typed name)."""
        # Box coordinates (same as in draw_white_box)
        box_width = 1200
        box_height = 340
        box_x = (self.width() - box_width) // 2
        box_y = 705

        # Create a new pixmap with just a white box (no pre-typed name)
        final_pixmap = QPixmap(box_width, box_height)
        final_pixmap.fill(Qt.white)

        # Draw only the user's pen strokes that fall within the box area
        painter = QPainter(final_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw user's pen strokes respecting stroke boundaries
        if len(self.pen_positions) > 1:
            pen = QPen(Qt.black, 20, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)

            # Add the end boundary
            stroke_boundaries = self.stroke_boundaries + [len(self.pen_positions)]

            # Draw each stroke separately
            for stroke_idx in range(len(stroke_boundaries) - 1):
                start_idx = stroke_boundaries[stroke_idx]
                end_idx = stroke_boundaries[stroke_idx + 1]

                # Draw lines within this stroke
                for i in range(start_idx + 1, end_idx):
                    x1, y1 = self.pen_positions[i - 1]
                    x2, y2 = self.pen_positions[i]

                    # Check if both points are within the white box area
                    if (box_x <= x1 <= box_x + box_width and box_y <= y1 <= box_y + box_height and
                            box_x <= x2 <= box_x + box_width and box_y <= y2 <= box_y + box_height):
                        # Convert coordinates to box-relative coordinates
                        rel_x1, rel_y1 = x1 - box_x, y1 - box_y
                        rel_x2, rel_y2 = x2 - box_x, y2 - box_y
                        painter.drawLine(rel_x1, rel_y1, rel_x2, rel_y2)

        painter.end()
        return final_pixmap

    def show_popup_with_home(self):
        """Show completion popup with home button."""
        popup = QDialog(self)
        popup.setWindowTitle("Next")
        popup.setFixedSize(500, 500)

        layout = QVBoxLayout()

        label = QLabel("Good Job!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 70px;
            }
        """)
        layout.addWidget(label)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(300)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 40px;          
            }
        """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)
        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        """Return to home screen from popup."""
        popup.close()
        self.open_main_screen()

    def generate_new_name(self):
        available = [name for name in self.puppy_names if name != self.current_puppy_name]
        self.current_puppy_name = random.choice(available)
        self.draw_white_box()  # redraw with updated name

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.drawing)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.drawing = QPixmap(self.size())
        self.drawing.fill(QColor(13, 190, 241))
        self.draw_white_box()  # redraw after resize

    def _start_drawing(self, pos, pressure=None):
        """Helper method to start drawing and track metrics"""
        current_time = time.time()

        if not self.is_drawing:
            self.pendown_count += 1
            self.is_drawing = True

            # Mark the start of a new stroke
            self.stroke_boundaries.append(len(self.pen_positions))

            # End air time, start paper time
            if self.air_start_time:
                self.air_time += current_time - self.air_start_time
            self.paper_start_time = current_time

        # Record position, timestamp, and pressure
        self.pen_positions.append((pos.x(), pos.y()))
        self.pen_timestamps.append(current_time)
        # Only add pressure if it's provided (tablet events), otherwise add 0
        self.pressure_readings.append(pressure if pressure is not None else 0)

    def _end_drawing(self):
        """Helper method to end drawing and track metrics"""
        if self.is_drawing:
            current_time = time.time()
            self.is_drawing = False

            # End paper time, start air time
            if self.paper_start_time:
                self.paper_time += current_time - self.paper_start_time
            self.air_start_time = current_time

    def mousePressEvent(self, event):
        # Check if click is on the next button
        if self.next_btn.geometry().contains(event.pos()):
            return  # Don't start drawing on the button

        self.last_point = event.pos()
        self._start_drawing(event.pos())  # No default pressure for mouse

    def mouseMoveEvent(self, event):
        # Check if mouse is over the next button
        if self.next_btn.geometry().contains(event.pos()):
            return  # Don't draw on the button

        # Only draw if left button is pressed AND we have a valid last point AND we're currently drawing
        if event.buttons() & Qt.LeftButton and self.last_point and self.is_drawing:
            painter = QPainter(self.drawing)
            pen = QPen(Qt.black, 20, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()

            # Track drawing metrics - just record position, don't call _start_drawing
            current_time = time.time()
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            self.pressure_readings.append(0)  # Mouse has no pressure

            self.update()

    def mouseReleaseEvent(self, event):
        self.last_point = None
        self._end_drawing()

    def tabletEvent(self, event: QTabletEvent):
        # Check if tablet event is on the next button
        if self.next_btn.geometry().contains(event.pos()):
            return  # Don't draw on the button

        if event.type() == QTabletEvent.TabletPress:
            self.last_point = event.pos()
            self._start_drawing(event.pos(), pressure=event.pressure())

        elif event.type() == QTabletEvent.TabletMove and self.last_point and self.is_drawing:
            painter = QPainter(self.drawing)
            pen = QPen(Qt.black, 20, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()

            # Track drawing metrics - just record position, don't call _start_drawing
            current_time = time.time()
            self.pen_positions.append((event.pos().x(), event.pos().y()))
            self.pen_timestamps.append(current_time)
            self.pressure_readings.append(event.pressure())

            self.update()

        elif event.type() == QTabletEvent.TabletRelease:
            self.last_point = None
            self._end_drawing()

        event.accept()

    def open_main_screen(self):
        # Only save if not already saved
        if not self.session_saved:
            self.save_image_and_log()
        self.hide()
        self.main_dialog.show()

class Level8_Screen(QMainWindow):
    def __init__(self, main_dialog, player_name):
        super().__init__()
        self.main_dialog = main_dialog
        self.player_name = player_name
        self.start_time = None
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"

        self.GAME_COLORS = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (255, 165, 0), (128, 0, 128)
        ]

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.hide_all_cards)

        self.flip_timer = QTimer()
        self.flip_timer.setSingleShot(True)
        self.flip_timer.timeout.connect(self.hide_unmatched_cards)

        self.setup_ui()
        self.initialize_game_state()
        self.create_cards()
        self.update_stats_display()
        self.start_preview_phase()

    def setup_ui(self):
        self.setWindowTitle("Level 8 - Memory Game")
        self.setMinimumSize(2000, 1100)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: rgb(233, 178, 99);")

        self.title_label = QLabel(f"Hey {self.player_name}, Welcome to the Memory Game", central_widget)
        self.title_label.setStyleSheet("font-size: 72px; font-weight: bold; color: black;")
        self.title_label.adjustSize()
        self.title_label.move(400, 20)

        self.stats_label = QLabel("Matches: 0/8", central_widget)
        self.stats_label.setStyleSheet("font-size: 50px; color: black;")
        self.stats_label.adjustSize()
        self.stats_label.move(10, 100)

        self.cards_widget = QWidget(central_widget)
        self.cards_widget.setGeometry(300, 120, 1500, 900)
        self.cards_layout = QGridLayout(self.cards_widget)
        self.cards_layout.setSpacing(30)
        self.cards_layout.setVerticalSpacing(50)

        self.instruction_label = QLabel("Click cards to find matching pairs!", central_widget)
        self.instruction_label.setStyleSheet("font-size: 36px; color: black;")
        self.instruction_label.resize(1100, 130)
        self.instruction_label.move(500, 990)

        home_btn = QPushButton("Home", central_widget)
        home_btn.setFixedWidth(200)
        home_btn.setFont(QFont("Arial", 16))
        home_btn.clicked.connect(self.open_main_screen)
        home_btn.move(10, 10)



    def show_win_popup(self):
        """Show win popup with restart and home buttons."""
        popup = QDialog(self)
        popup.setWindowTitle("Congratulations!")
        popup.setFixedSize(600, 500)

        layout = QVBoxLayout()

        label = QLabel(f"\U0001F389 You Win!\nWell done, {self.player_name}!")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: Black;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 40px;
                margin: 20px;
            }
        """)
        layout.addWidget(label)

        # Button container
        button_layout = QHBoxLayout()

        restart_btn = QPushButton("Restart Game")
        restart_btn.setFixedWidth(250)
        restart_btn.clicked.connect(lambda: self.restart_from_popup(popup))
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: lightgreen;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 30px;          
            }
        """)

        home_btn = QPushButton("Home")
        home_btn.setFixedWidth(250)
        home_btn.clicked.connect(lambda: self.return_home_from_popup(popup))
        home_btn.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 30px;              
                border-color: beige;
                padding: 6px;
                color: Black;
                font-weight: bold;
                font-size: 30px;          
            }
        """)

        button_layout.addWidget(restart_btn)
        button_layout.addWidget(home_btn)
        layout.addLayout(button_layout)

        popup.setLayout(layout)
        popup.exec_()

    def restart_from_popup(self, popup):
        """Restart game from popup."""
        popup.accept()
        self.restart_game()

    def return_home_from_popup(self, popup):
        """Return to home screen from popup."""
        popup.accept()
        self.open_main_screen()

    def save_results_to_excel(self, total_time):
        """Save player results to Excel file."""
        try:
            excel_path = os.path.join(self.SAVE_FOLDER, "Level1Results.xlsx")

            # Create directory if it doesn't exist
            os.makedirs(self.SAVE_FOLDER, exist_ok=True)

            # Load or create workbook
            if os.path.exists(excel_path):
                workbook = openpyxl.load_workbook(excel_path)
            else:
                workbook = Workbook()
                # Remove default sheet and create our sheet
                workbook.remove(workbook.active)

            sheet = workbook["Results"]

            # Find next empty row
            row = sheet.max_row + 1

            # Add data
            sheet[f'A{row}'] = self.player_name
            sheet[f'C{row}'] = "Level 8"
            sheet[f'D{row}'] = round(total_time, 2)

            # Save workbook
            workbook.save(excel_path)
            print(f"Results saved to {excel_path}")

        except Exception as e:
            print(f"Error saving results: {e}")

    def open_main_screen(self):
        """Open the main screen."""
        self.hide()
        self.main_dialog.show()

    def initialize_game_state(self):
        self.first_card = None
        self.second_card = None
        self.matches = 0
        self.attempts = 0
        self.game_won = False
        self.show_initial = True
        self.allow_clicks = True
        self.start_time = time.time()  # Start timing when game begins

    def create_cards(self):
        shapes = ['circle', 'square', 'triangle', 'diamond', 'star', 'hexagon', 'heart', 'cross']
        colors = self.GAME_COLORS[:8]
        pairs = [{'shape': shapes[i], 'color': colors[i]} for i in range(8)] * 2
        random.shuffle(pairs)

        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        self.cards = []
        for i, pair in enumerate(pairs):
            card = QPushButton()
            card.shape = pair['shape']
            card.color = pair['color']
            card.revealed = False
            card.matched = False
            card.setFixedSize(300, 180)
            card.paintEvent = lambda e, c=card: self.card_paint(c, e)
            card.update_appearance = lambda c=card: self.update_appearance(c)
            card.update_appearance()
            card.clicked.connect(lambda _, c=card: self.handle_card_click(c))
            self.cards.append(card)
            self.cards_layout.addWidget(card, i // 4, i % 4)

    def update_appearance(self, card):
        if card.revealed or card.matched:
            card.setText("")
            card.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 3px solid black;
                    border-radius: 5px;
                }
            """)
        else:
            card.setText("\u2022    \u2022    \u2022\n\u2022    \u2022    \u2022\n\u2022    \u2022    \u2022")
            card.setStyleSheet("""
                QPushButton {
                    background-color: rgb(43, 91, 203);
                    color: rgb(99, 197, 233);
                    border: 3px solid black;
                    border-radius: 5px;
                    font-size: 50px;
                    font-weight: bold;
                }
            """)

    def card_paint(self, card, event):
        QPushButton.paintEvent(card, event)
        if card.revealed or card.matched:
            painter = QPainter(card)
            painter.setRenderHint(QPainter.Antialiasing)
            color = QColor(*card.color)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 2))

            aw, ah = card.width() * 0.8, card.height() * 0.8
            size = int(min(aw, ah) / 2)
            cx, cy = card.width() // 2, card.height() // 2
            self.draw_shape(painter, cx, cy, size, card.shape, color)

    def draw_shape(self, painter, cx, cy, size, shape, color):
        if shape == 'circle':
            painter.drawEllipse(cx - size, cy - size, size * 2, size * 2)
        elif shape == 'square':
            painter.drawRect(cx - size, cy - size, size * 2, size * 2)
        elif shape == 'triangle':
            points = [QPoint(cx, cy - size), QPoint(cx - size, cy + size), QPoint(cx + size, cy + size)]
            painter.drawPolygon(QPolygon(points))
        elif shape == 'diamond':
            points = [QPoint(cx, cy - size), QPoint(cx + size, cy), QPoint(cx, cy + size), QPoint(cx - size, cy)]
            painter.drawPolygon(QPolygon(points))
        elif shape == 'star':
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                r = size if i % 2 == 0 else size * 0.5
                x = cx + r * math.cos(angle - math.pi / 2)
                y = cy + r * math.sin(angle - math.pi / 2)
                points.append(QPoint(int(x), int(y)))
            painter.drawPolygon(QPolygon(points))
        elif shape == 'hexagon':
            points = [QPoint(int(cx + size * math.cos(i * math.pi / 3)), int(cy + size * math.sin(i * math.pi / 3))) for
                      i in range(6)]
            painter.drawPolygon(QPolygon(points))
        elif shape == 'heart':
            path = QPainterPath()
            path.moveTo(cx, cy + size * 1.2)
            path.cubicTo(cx + size * 2.6, cy - size * 0.4, cx + size * 0.5, cy - size - 55, cx, cy - size * 0.4)
            path.cubicTo(cx - size * 0.5, cy - size - 55, cx - size * 2.6, cy - size * 0.4, cx, cy + size * 1.2)
            painter.fillPath(path, QBrush(color))
        elif shape == 'cross':
            painter.drawRect(cx - size // 4, cy - size, size // 2, size * 2)
            painter.drawRect(cx - size, cy - size // 4, size * 2, size // 2)

    def start_preview_phase(self):
        self.show_initial = True
        for card in self.cards:
            card.revealed = True
            card.update_appearance()
        self.update_instruction_text()
        self.preview_timer.start(6000)

    def hide_all_cards(self):
        self.show_initial = False
        for card in self.cards:
            card.revealed = False
            card.update_appearance()
        self.update_instruction_text()
        # Start timing after preview phase ends
        if self.start_time is None:
            self.start_time = time.time()

    def handle_card_click(self, card):
        if self.game_won or self.show_initial or not self.allow_clicks or card.revealed or card.matched:
            return
        card.revealed = True
        card.update_appearance()
        if self.first_card is None:
            self.first_card = card
        elif self.second_card is None:
            self.second_card = card
            self.allow_clicks = False
            self.attempts += 1
            self.update_stats_display()
            QTimer.singleShot(500, self.check_for_match)

    def check_for_match(self):
        if self.first_card and self.second_card:
            if (self.first_card.shape == self.second_card.shape and
                    self.first_card.color == self.second_card.color):
                self.first_card.matched = True
                self.second_card.matched = True
                self.matches += 1
                self.first_card = None
                self.second_card = None
                self.allow_clicks = True
                self.update_stats_display()
                if self.matches == 8:
                    self.game_won = True
                    # Calculate total time and save results
                    end_time = time.time()
                    total_time = end_time - self.start_time
                    self.save_results_to_excel(total_time)
                    # Show win popup instead of updating instruction text
                    self.show_win_popup()
            else:
                self.flip_timer.start(1000)

    def hide_unmatched_cards(self):
        if self.first_card and self.second_card:
            self.first_card.revealed = False
            self.second_card.revealed = False
            self.first_card.update_appearance()
            self.second_card.update_appearance()
            self.first_card = None
            self.second_card = None
        self.allow_clicks = True

    def update_stats_display(self):
        self.stats_label.setText(f"Matches: {self.matches}/8")

    def update_instruction_text(self):
        if self.show_initial:
            self.instruction_label.setText("Memorize the pairs!")
            self.instruction_label.setStyleSheet("font-size: 54px; color: red; margin: 20px;")
        else:
            self.instruction_label.setText("Click cards to find matching pairs!")
            self.instruction_label.setStyleSheet("font-size: 54px; color: black; margin: 20px;")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R and self.game_won:
            self.restart_game()
        super().keyPressEvent(event)

    def restart_game(self):
        self.initialize_game_state()
        self.create_cards()
        self.update_stats_display()
        self.start_preview_phase()

    def open_main_screen(self):
        self.hide()
        self.main_dialog.show()


class Name_Screen(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(2000, 1100)
        self.resize(2000, 1100)

        # Background setup
        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        self.pixmap = QPixmap("back2.jpg")
        if self.pixmap.isNull():
            print("Error: 'back2.jpg' not found or could not be loaded.")
        else:
            self.bg_label.setPixmap(self.pixmap)
            self.bg_label.resize(self.size())

        # Next button
        self.button = QPushButton("Next", self)
        self.button.resize(300, 150)
        self.button.move(1750, 950)
        self.button.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)
        self.button.clicked.connect(self.proceed_to_game_menu)

        # Back button
        self.button1 = QPushButton("Back", self)
        self.button1.resize(200, 100)
        self.button1.move(0, 0)
        self.button1.setStyleSheet("""
            QPushButton {
            background-color: black;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 50px;
            }
        """)
        self.button1.clicked.connect(self.back_button)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Please enter your name to begin your adventure!", self)
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setStyleSheet("background-color: black; color: #ecf0f1;font-weight: bold;")
        title.move(10, 340)
        layout.addWidget(title)

        # Name input
        input_layout = QHBoxLayout()
        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        name_label = QLabel("Name:", self)
        name_label.setFont(QFont("Arial", 25))
        name_label.setStyleSheet("background-color: black;font-weight: bold; color: #ecf0f1; margin: 30px;")
        name_label.resize(290, 150)
        name_label.move(310, 425)
        layout.addWidget(name_label)

        self.name_input = QLineEdit(self)
        self.name_input.setFont(QFont("Arial", 25))
        self.name_input.setFixedHeight(100)
        self.name_input.setFixedWidth(1000)
        self.name_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 2px solid #3498db;
                    border-radius: 20px;
                    background-color: black;
                    font-weight: bold;
                    color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #2ecc71;
                    background-color: black;
                }
            """)
        self.name_input.setPlaceholderText("Enter your name here...")
        self.name_input.textChanged.connect(self.check_input)
        self.name_input.returnPressed.connect(self.proceed_to_game_menu)
        self.name_input.move(580, 450)
        layout.addWidget(self.name_input)

    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            self.bg_label.setPixmap(self.pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))
            self.bg_label.resize(self.size())

    def check_input(self):
        self.button.setEnabled(bool(self.name_input.text().strip()))

    def proceed_to_game_menu(self):
        if self.name_input.text().strip():
            self.hide()
            self.dialog = QDialog()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self.dialog, self.name_input.text().strip())
            self.dialog.exec_()

    def back_button(self):
        self.hide()
        self.main_menu = MainMenuScreen()
        self.main_menu.show()


class MainMenuScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jumanji")
        self.setMinimumSize(2000, 1100)
        self.resize(2000, 1100)

        self.bg1_label = QLabel(self)
        self.bg1_label.setScaledContents(True)
        self.original_pixmap = QPixmap("back.png")
        if self.original_pixmap.isNull():
            print("Error: 'back.png' not found or could not be loaded.")
        else:
            self.bg1_label.setPixmap(self.original_pixmap)
            self.bg1_label.resize(self.size())

        # Title Label
        self.Tlabel = QLabel("Welcome to Jumanji", self)
        self.Tlabel.setFont(QFont("Fantasy", 60))
        self.Tlabel.setStyleSheet("color: white;font-weight: bold;")
        self.Tlabel.setAlignment(Qt.AlignCenter)
        self.Tlabel.setMinimumSize(2000,900)
        self.Tlabel.move(0,100)
        # Next button
        self.button = QPushButton("Next", self)
        self.button.resize(300, 150)
        self.button.move(1750, 950)
        self.button.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 50px;
            }
        """)
        self.button.clicked.connect(self.open_name_screen)

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            self.bg1_label.setPixmap(self.original_pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))
            self.bg1_label.resize(self.size())
        super().resizeEvent(event)

    def open_name_screen(self):
        self.hide()
        self.name_screen = Name_Screen()
        self.name_screen.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenuScreen()
    window.show()
    sys.exit(app.exec_())
