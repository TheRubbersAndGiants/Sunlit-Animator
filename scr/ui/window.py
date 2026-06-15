import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from ui.canvas import AnimationCanvas
from ui.properties import PropertiesPanel
from ui.timeline_view import TimelineView

class SunlitAnimatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sunlit Animator")
        self.resize(1280, 720)
        self.setStyleSheet("background-color: #121212;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        top_splitter.setStyleSheet("QSplitter::handle { background-color: #262626; }")

        self.canvas = AnimationCanvas()
        self.properties = PropertiesPanel()
        
        self.properties.canvas_color_btn.clicked.disconnect()
        self.properties.canvas_color_btn.clicked.connect(self.handle_canvas_color_change)

        top_splitter.addWidget(self.canvas)
        top_splitter.addWidget(self.properties)
        top_splitter.setSizes([900, 280])

        self.timeline = TimelineView()

        main_layout.addWidget(top_splitter, stretch=1)
        main_layout.addWidget(self.timeline, stretch=0)

    def handle_canvas_color_change(self):
        from PyQt6.QtWidgets import QColorDialog
        color = QColorDialog.getColor(Qt.GlobalColor.white, self, "Select Stage Color")
        if color.isValid():
            self.canvas.set_canvas_color(color)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.timeline.move_frame(-1)
        elif event.key() == Qt.Key.Key_Right:
            self.timeline.move_frame(1)
        elif event.key() == Qt.Key.Key_Up:
            self.timeline.move_layer(-1)
        elif event.key() == Qt.Key.Key_Down:
            self.timeline.move_layer(1)
        elif event.key() == Qt.Key.Key_9:
            pass
        elif event.key() == Qt.Key.Key_0:
            pass
        else:
            super().keyPressEvent(event)
