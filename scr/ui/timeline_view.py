import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class TimelineView(QWidget):
    frame_changed = pyqtSignal(int)
    layer_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_frame = 0
        self.current_layer = 0
        self.total_frames = 60
        self.total_layers = 3
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(180)
        self.setStyleSheet("""
            QWidget {
                background-color: #262626;
                color: #E0E0E0;
                font-family: 'Segoe UI', sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: #262626;
            }
            QFrame#TrackBackground {
                background-color: #1A1A1A;
                border: 1px solid #333333;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)

        self.layer_panel = QVBoxLayout()
        self.layer_panel.setSpacing(2)
        self.refresh_layers()
        main_layout.addLayout(self.layer_panel)

        self.scroll_area = QScrollArea()
        self.scroll_container = QWidget()
        self.track_layout = QVBoxLayout(self.scroll_container)
        self.track_layout.setSpacing(2)
        self.track_layout.setContentsMargins(0, 0, 0, 0)
        
        self.refresh_tracks()
        
        self.scroll_area.setWidget(self.scroll_container)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def refresh_layers(self):
        while self.layer_panel.count():
            item = self.layer_panel.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for i in range(self.total_layers):
            lbl = QLabel(f"Layer {self.total_layers - i}")
            lbl.setFixedSize(100, 24)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if i == self.current_layer:
                lbl.setStyleSheet("background-color: #333333; border: 1px solid #00A3FF; color: #808080;")
            else:
                lbl.setStyleSheet("background-color: #1E1E1E; border: 1px solid #333333; color: #00A3FF;")
            self.layer_panel.addWidget(lbl)
        self.layer_panel.addStretch()

    def refresh_tracks(self):
        while self.track_layout.count():
            item = self.track_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for l in range(self.total_layers):
            row = QHBoxLayout()
            row.setSpacing(1)
            row.setContentsMargins(0, 0, 0, 0)
            for f in range(self.total_frames):
                frame_box = QFrame()
                frame_box.setFixedSize(15, 24)
                frame_box.setObjectName("TrackBackground")
                
                if f == self.current_frame and l == self.current_layer:
                    frame_box.setStyleSheet("background-color: #333333; border: 1px solid #808080;")
                else:
                    frame_box.setStyleSheet("background-color: #262626; border: 1px solid #333333;")
                
                row.addWidget(frame_box)
            row.addStretch()
            self.track_layout.addLayout(row)
        self.track_layout.addStretch()

    def move_frame(self, direction):
        new_frame = self.current_frame + direction
        if 0 <= new_frame < self.total_frames:
            self.current_frame = new_frame
            self.refresh_tracks()
            self.frame_changed.emit(self.current_frame)

    def move_layer(self, direction):
        new_layer = self.current_layer + direction
        if 0 <= new_layer < self.total_layers:
            self.current_layer = new_layer
            self.refresh_layers()
            self.refresh_tracks()
            self.layer_changed.emit(self.current_layer)
