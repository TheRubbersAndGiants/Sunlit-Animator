import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QLineEdit, QListWidget, QPushButton, 
                             QFrame, QColorDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

class PropertiesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
            }
            QLabel {
                font-weight: bold;
                color: #808080;
            }
            QLineEdit {
                background-color: #141414;
                border: 1px solid #333333;
                border-radius: 3px;
                color: #E0E0E0;
                padding: 3px;
            }
            QLineEdit:focus {
                border: 1px solid #00A3FF;
            }
            QSlider::groove:horizontal {
                border: 1px solid #333333;
                height: 4px;
                background: #141414;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #808080;
                border: 1px solid #333333;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QListWidget {
                background-color: #141414;
                border: 1px solid #333333;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #333333;
                color: #808080;
                border: 1px solid #00A3FF;
            }
            QPushButton {
                background-color: #262626;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                border: 1px solid #00A3FF;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        stage_label = QLabel("STAGE PROPERTIES")
        main_layout.addWidget(stage_label)

        canvas_color_layout = QHBoxLayout()
        canvas_color_label = QLabel("Canvas Color:")
        self.canvas_color_btn = QPushButton("Change")
        self.canvas_color_btn.clicked.connect(self.pick_canvas_color)
        canvas_color_layout.addWidget(canvas_color_label)
        canvas_color_layout.addWidget(self.canvas_color_btn)
        main_layout.addLayout(canvas_color_layout)

        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setStyleSheet("background-color: #333333;")
        main_layout.addWidget(divider1)

        object_label = QLabel("OBJECTS ON FRAME")
        main_layout.addWidget(object_label)

        self.object_list = QListWidget()
        self.object_list.itemDoubleClicked.connect(self.rename_object)
        main_layout.addWidget(self.object_list)

        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("background-color: #333333;")
        main_layout.addWidget(divider2)

        transform_label = QLabel("TRANSFORM & FILTERS")
        main_layout.addWidget(transform_label)

        brush_layout = QHBoxLayout()
        brush_label = QLabel("Brush Size:")
        self.brush_input = QLineEdit("10")
        self.brush_input.setFixedWidth(40)
        self.brush_input.setValidator(QIntValidator(1, 200))
        self.brush_slider = QSlider(Qt.Orientation.Horizontal)
        self.brush_slider.setRange(1, 200)
        self.brush_slider.setValue(10)
        
        self.brush_input.textChanged.connect(self.sync_input_to_slider)
        self.brush_slider.valueChanged.connect(self.sync_slider_to_input)
        
        brush_layout.addWidget(brush_label)
        brush_layout.addWidget(self.brush_input)
        brush_layout.addWidget(self.brush_slider)
        main_layout.addLayout(brush_layout)

        ease_layout = QHBoxLayout()
        ease_label = QLabel("Ease Value:")
        self.ease_input = QLineEdit("0")
        self.ease_input.setFixedWidth(40)
        self.ease_input.setValidator(QIntValidator(-1000, 1000))
        self.ease_slider = QSlider(Qt.Orientation.Horizontal)
        self.ease_slider.setRange(-1000, 1000)
        self.ease_slider.setValue(0)
        
        self.ease_input.textChanged.connect(self.sync_ease_input)
        self.ease_slider.valueChanged.connect(self.sync_ease_slider)
        
        ease_layout.addWidget(ease_label)
        ease_layout.addWidget(self.ease_input)
        ease_layout.addWidget(self.ease_slider)
        main_layout.addLayout(ease_layout)

        self.reset_ease_btn = QPushButton("Reset Ease")
        self.reset_ease_btn.clicked.connect(self.reset_easing)
        main_layout.addWidget(self.reset_ease_btn)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def sync_input_to_slider(self, text):
        if text:
            val = int(text)
            self.brush_slider.setValue(val)

    def sync_slider_to_input(self, value):
        self.brush_input.setText(str(value))

    def sync_ease_input(self, text):
        if text:
            try:
                val = int(text)
                if -1000 <= val <= 1000:
                    self.brush_slider.setValue(val)
            except ValueError:
                pass

    def sync_ease_slider(self, value):
        self.ease_input.setText(str(value))

    def reset_easing(self):
        self.ease_slider.setValue(0)

    def rename_object(self, item):
        pass

    def pick_canvas_color(self):
        color = QColorDialog.getColor(Qt.GlobalColor.white, self, "Select Stage Color")
        if color.isValid():
            pass
