import sys
import math
import os
import numpy as np
from PIL import Image, ImageQt
import pandas as pd
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as XLImage

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
    def setupUi(self, Dialog, player_name, cursor_pixmap):

        self.Dialog = Dialog
        self.player_name = player_name
        self.cursor_pixmap = cursor_pixmap

        Dialog.setObjectName("Dialog")
        Dialog.resize(2000, 1100)
        Dialog.setWindowTitle(f"Game Menu - Welcome {player_name}!")


        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 400, 400))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #3498db;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 100, 400, 400))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(1000, 100, 400, 400))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(1450, 100, 400, 400))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e73c82;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 600, 400, 400))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #ff99ff;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(550, 600, 400, 400))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #3cd8e7;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.setGeometry(QtCore.QRect(1000, 600, 400, 400))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #e7a13c;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.setGeometry(QtCore.QRect(1450, 600, 400, 400))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("""
            QPushButton {
                border-radius: 200px;
                background-color: #a13ce7;
                color: white;
                font-weight: bold;
                font-size: 50px;
            }
        """)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(self.show_Level1Screen)
        self.pushButton_2.clicked.connect(self.show_Level2Screen)
        self.pushButton_3.clicked.connect(self.show_Level3Screen)
        self.pushButton_4.clicked.connect(self.show_Level4Screen)
        self.pushButton_5.clicked.connect(self.show_Level5Screen)
        self.pushButton_6.clicked.connect(self.show_Level6Screen)


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

    def show_Level1Screen(self):
        self.pen_screen = Level1_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen_screen.show()

    def show_Level2Screen(self):
        self.pen2_screen = Level2_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen2_screen.show()
    def show_Level3Screen(self):
        self.pen3_screen = Level3_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen3_screen.show()

    def show_Level4Screen(self):
        self.pen_screen = Level4_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen_screen.show()

    def show_Level5Screen(self):
        self.pen2_screen = Level5_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen2_screen.show()
    def show_Level6Screen(self):
        self.pen3_screen = Level6_Screen(self.Dialog, self.player_name, self.cursor_pixmap)
        self.Dialog.hide()
        self.pen3_screen.show()


class Level1_Screen(QWidget):
    def __init__(self, main_dialog, player_name, cursor_pixmap):
        super().__init__()

        self.player_name = player_name
        self.main_dialog = main_dialog
        self.SAVE_FOLDER = r"C:\Users\Hooria\PycharmProjects\Project4\.venv\city_img"
        self.EXCEL_PATH = os.path.join(self.SAVE_FOLDER, "Level1Results.xlsx")

        self.setWindowTitle("Level 1 - Pen Input")
        self.setMinimumSize(2000, 1100)
        self.setMouseTracking(True)

        self.reference_layer = QPixmap(self.size())  # Wave layer
        self.reference_layer.fill(Qt.transparent)

        self.drawing = QPixmap(self.size())  # User layer
        self.drawing.fill(Qt.darkGreen)

        cursor_for_game = cursor_pixmap.scaled(200, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.setCursor(QCursor(cursor_for_game))

        self.last_point = None

        layout = QVBoxLayout()

        self.next_btn = QPushButton("Next",self)
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
        self.draw_sin_wave()

    def draw_sin_wave(self):
        painter = QPainter(self.reference_layer)
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        amplitude = height // 7
        mid_y = height // 2

        prev_point = QPoint(0, mid_y)
        for x in range(1, width):
            y = mid_y - int(math.sin(x * 0.01) * amplitude)
            curr_point = QPoint(x, y)
            painter.drawLine(prev_point, curr_point)
            prev_point = curr_point

    def handle_next(self):
        self.save_image_and_log()
        self.show_popup_with_home()

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
                          } """)
        layout.addWidget(home_btn, alignment=Qt.AlignCenter)

        popup.setLayout(layout)
        popup.exec_()

    def return_home_from_popup(self, popup):
        popup.accept()
        self.open_main_screen()

    def save_image_and_log(self):
        if not os.path.exists(self.SAVE_FOLDER):
            os.makedirs(self.SAVE_FOLDER)

        # Ensure Excel file exists
        if not os.path.exists(self.EXCEL_PATH):
            wb = Workbook()
            ws = wb.active
            ws.title = "Results"
            ws.append(["Player Name", "Processed Image", "Level"])
            wb.save(self.EXCEL_PATH)

        wb = load_workbook(self.EXCEL_PATH)
        ws = wb["Results"]

        # Count existing entries for this player_name
        existing_entries = [cell.value for cell in ws['A'] if cell.value == self.player_name]
        session_id = len(existing_entries) + 1
        suffix = f"_{session_id}"

        # --- File paths ---
        processed_path = os.path.join(self.SAVE_FOLDER, f"{self.player_name}_processed{suffix}.png")
        excel_img_path = os.path.join(self.SAVE_FOLDER, f"{self.player_name}_excel{suffix}.png")

        # Save current drawing pixmap temporarily to process
        temp_path = os.path.join(self.SAVE_FOLDER, "temp.png")
        self.drawing.save(temp_path)

        # Process image (grayscale, standardize, rescale)
        gray = Image.open(temp_path).convert('L')
        img_array = np.array(gray).astype(np.float32)
        normalized = img_array / 255.0
        mean = normalized.mean()
        std = normalized.std() or 1
        standardized = (normalized - mean) / std
        rescaled = ((standardized - standardized.min()) / (standardized.max() - standardized.min()) * 255).astype(
            np.uint8)
        Image.fromarray(rescaled).save(processed_path)

        # Remove the temp image file
        os.remove(temp_path)

        # Log to Excel
        row = ws.max_row + 1
        ws.cell(row=row, column=1).value = self.player_name
        ws.cell(row=row, column=3).value = "Level 1"
        try:
            thumbnail_img = Image.open(processed_path)
            thumbnail_img.thumbnail((150, 75), Image.LANCZOS)
            thumbnail_img.save(excel_img_path)

            ws.row_dimensions[row].height = 60
            ws.column_dimensions['B'].width = 25
            time.sleep(0.1)

            xl_img = XLImage(excel_img_path)
            xl_img.width = 150
            xl_img.height = 75
            xl_img.anchor = f"B{row}"
            ws.add_image(xl_img)

            wb.save(self.EXCEL_PATH)
        except Exception as e:
            print(f"Excel insert failed: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.drawing)
        painter.drawPixmap(0, 0, self.reference_layer)

    def resizeEvent(self, event):
        new_drawing = QPixmap(self.size())
        new_drawing.fill(Qt.darkMagenta)
        QPainter(new_drawing).drawPixmap(0, 0, self.drawing)
        self.drawing = new_drawing

        new_reference = QPixmap(self.size())
        new_reference.fill(Qt.transparent)
        QPainter(new_reference).drawPixmap(0, 0, self.reference_layer)
        self.reference_layer = new_reference

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_point:
            painter = QPainter(self.drawing)
            pen = QPen(Qt.black, 10)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.last_point = None

    def tabletEvent(self, event: QTabletEvent):
        if event.type() == QTabletEvent.TabletPress:
            self.last_point = event.pos()
        elif event.type() == QTabletEvent.TabletMove and self.last_point is not None:
            painter = QPainter(self.drawing)
            pressure = event.pressure()
            pen = QPen(Qt.darkRed, pressure * 50)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()
        elif event.type() == QTabletEvent.TabletRelease:
            self.last_point = None
        event.accept()

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
        self.pixmap = QPixmap("back2.jpg")  # Match file name exactly
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
        self.button.clicked.connect(self.proceed_to_cursor_selection)

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
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("background-color: black; color: #ecf0f1; margin: 30px;")
        title.move(150,300)
        layout.addWidget(title)

        # Name input
        input_layout = QHBoxLayout()
        input_widget = QWidget()
        input_widget.setLayout(input_layout)

        name_label = QLabel("Name:", self)
        name_label.setFont(QFont("Arial", 16))
        name_label.setStyleSheet("background-color: black; color: #ecf0f1; margin: 30px;")
        name_label.resize(200,110)
        name_label.move(300,405)
        layout.addWidget(name_label)

        self.name_input = QLineEdit(self)
        self.name_input.setFont(QFont("Arial", 16))
        self.name_input.setFixedHeight(80)
        self.name_input.setFixedWidth(1000)  # Make input box wider
        self.name_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 2px solid #3498db;
                    border-radius: 20px;
                    background-color: black;
                    color: white;
                }
                QLineEdit:focus {
                    border: 2px solid #2ecc71;
                    background-color: black;
                }
            """)
        self.name_input.setPlaceholderText("Enter your name here...")
        self.name_input.textChanged.connect(self.check_input)
        self.name_input.returnPressed.connect(self.proceed_to_cursor_selection)
        self.name_input.move(510, 420)
        layout.addWidget(self.name_input)

    def resizeEvent(self, event):
        if not self.pixmap.isNull():
            self.bg_label.setPixmap(self.pixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))
            self.bg_label.resize(self.size())
    def check_input(self):
        self.button.setEnabled(bool(self.name_input.text().strip()))
    def proceed_to_cursor_selection(self):
        if self.name_input.text().strip():
            self.hide()
            self.cursor_screen = CursorSelectionScreen( self.name_input.text().strip())
            self.cursor_screen.show()

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
        self.Tlabel.setFont(QFont("Fantasy", 50))
        self.Tlabel.setStyleSheet("color: white;")
        self.Tlabel.resize(1300, 200)
        self.Tlabel.move(450, 450)

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
