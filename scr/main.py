import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.window import SunlitAnimatorWindow
from core.timeline import TimelineModel

class SunlitAnimatorApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.timeline_model = TimelineModel()
        self.main_window = SunlitAnimatorWindow()
        self.connect_architecture()
        self.main_window.show()

    def connect_architecture(self):
        self.main_window.timeline.frame_changed.connect(self.handle_frame_switch)
        self.main_window.timeline.layer_changed.connect(self.handle_layer_switch)
        
        self.main_window.keyPressEvent = self.override_key_press

    def handle_frame_switch(self, frame_index):
        current_layer = self.main_window.timeline.current_layer
        active_assets = self.timeline_model.evaluate_at_frame(current_layer, frame_index)
        
        self.main_window.properties.object_list.clear()
        for obj in active_assets:
            self.main_window.properties.object_list.addItem(obj.name)
            
        self.main_window.update()

    def handle_layer_switch(self, layer_index):
        current_frame = self.main_window.timeline.current_frame
        active_assets = self.timeline_model.evaluate_at_frame(layer_index, current_frame)
        
        self.main_window.properties.object_list.clear()
        for obj in active_assets:
            self.main_window.properties.object_list.addItem(obj.name)
            
        self.main_window.update()

    def override_key_press(self, event):
        from PyQt6.QtCore import Qt
        
        current_frame = self.main_window.timeline.current_frame
        current_layer = self.main_window.timeline.current_layer

        if event.key() == Qt.Key.Key_Left:
            self.main_window.timeline.move_frame(-1)
        elif event.key() == Qt.Key.Key_Right:
            self.main_window.timeline.move_frame(1)
        elif event.key() == Qt.Key.Key_Up:
            self.main_window.timeline.move_layer(-1)
        elif event.key() == Qt.Key.Key_Down:
            self.main_window.timeline.move_layer(1)
            
        elif event.key() == Qt.Key.Key_9:
            next_keyframe_match = current_frame + 10
            self.timeline_model.add_tween(current_layer, current_frame, next_keyframe_match, "purple")
            self.main_window.timeline.refresh_tracks()
            
        elif event.key() == Qt.Key.Key_0:
            next_keyframe_match = current_frame + 10
            self.timeline_model.convert_to_frame_by_frame(current_layer, current_frame, next_keyframe_match)
            self.main_window.timeline.refresh_tracks()
            
        else:
            super(SunlitAnimatorWindow, self.main_window).keyPressEvent(event)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    app = SunlitAnimatorApp(sys.argv)
    sys.exit(app.exec())
