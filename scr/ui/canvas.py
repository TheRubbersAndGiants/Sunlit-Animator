import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen

class AnimationCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas_color = QColor("#FFFFFF")
        self.pan_offset = QPoint(0, 0)
        self.zoom_level = 1.0
        self.last_mouse_pos = QPoint(0, 0)
        self.is_panning = False
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #121212;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.translate(self.width() / 2 + self.pan_offset.x(), self.height() / 2 + self.pan_offset.y())
        painter.scale(self.zoom_level, self.zoom_level)

        stage_w = 800
        stage_h = 450
        painter.fillRect(int(-stage_w / 2), int(-stage_h / 2), stage_w, stage_h, self.canvas_color)
        
        painter.setPen(QPen(QColor("#00A3FF"), 1))
        painter.drawRect(int(-stage_w / 2), int(-stage_h / 2), stage_w, stage_h)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.is_panning = True
            self.last_mouse_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.position().toPoint() - self.last_mouse_pos
            self.pan_offset += delta
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.is_panning = False

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        if angle > 0:
            self.zoom_level *= 1.1
        else:
            self.zoom_level /= 1.1
        self.update()

    def set_canvas_color(self, color):
        self.canvas_color = color
        self.update()
