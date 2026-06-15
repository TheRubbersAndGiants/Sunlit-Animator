import os
import shutil
import json
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import QSize

class AnimationExporter:
    def __init__(self, timeline_model, canvas_renderer):
        self.timeline = timeline_model
        self.renderer = canvas_renderer

    def export_png_sequence(self, output_directory, width=1920, height=1080):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for frame_idx in range(self.timeline.total_frames):
            image = QImage(QSize(width, height), QImage.Format.Format_ARGB32)
            image.fill(0)
            
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            self.renderer.render_frame_to_painter(painter, frame_idx, width, height)
            painter.end()

            filename = f"frame_{frame_idx:04d}.png"
            filepath = os.path.join(output_directory, filename)
            image.save(filepath, "PNG")

    def export_quicktime(self, output_filepath, width=1920, height=1080, fps=24):
        temp_dir = os.path.join(os.path.dirname(output_filepath), "_temp_sequence")
        self.export_png_sequence(temp_dir, width, height)

        try:
            import cv2
            import numpy as np

            fourcc = cv2.VideoWriter_fourcc(*'qdrw')
            video_writer = cv2.VideoWriter(output_filepath, fourcc, fps, (width, height))

            for frame_idx in range(self.timeline.total_frames):
                filename = f"frame_{frame_idx:04d}.png"
                frame_path = os.path.join(temp_dir, filename)
                
                img = cv2.imread(frame_path)
                video_writer.write(img)

            video_writer.release()
        except ImportError:
            pass
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def save_sunap_project(self, target_zip_path, canvas_color_hex):
        temp_project_dir = os.path.join(os.path.dirname(target_zip_path), "_temp_project")
        if not os.path.exists(temp_project_dir):
            os.makedirs(temp_project_dir)

        assets_dir = os.path.join(temp_project_dir, "assets")
        os.makedirs(assets_dir)

        project_data = {
            "canvas_color": canvas_color_hex,
            "total_frames": self.timeline.total_frames,
            "layers": []
        }

        for layer in self.timeline.layers:
            layer_dict = {
                "name": layer.name,
                "is_frame_by_frame": layer.is_frame_by_frame,
                "keyframes": {}
            }
            
            for idx, kf in layer.keyframes.items():
                kf_dict = {
                    "frame_type": kf.frame_type,
                    "ease_value": kf.ease_value,
                    "objects": []
                }
                
                for obj in kf.objects:
                    from core.engine import ImportedBitmap, VectorStroke
                    if isinstance(obj, ImportedBitmap):
                        base_name = os.path.basename(obj.filepath)
                        dest_path = os.path.join(assets_dir, base_name)
                        if os.path.exists(obj.filepath) and not os.path.exists(dest_path):
                            shutil.copy(obj.filepath, dest_path)
                            
                        kf_dict["objects"].append({
                            "type": "bitmap",
                            "name": obj.name,
                            "filepath": os.path.join("assets", base_name),
                            "warp_grid": obj.warp_grid
                        })
                    elif isinstance(obj, VectorStroke):
                        kf_dict["objects"].append({
                            "type": "vector_stroke",
                            "name": obj.name,
                            "size": obj.size,
                            "points": obj.points
                        })
                        
                layer_dict["keyframes"][str(idx)] = kf_dict
                
            project_data["layers"].append(layer_dict)

        meta_path = os.path.join(temp_project_dir, "project.json")
        with open(meta_path, "w") as f:
            json.dump(project_data, f, indent=4)

        base_output = target_zip_path.replace(".sunap", "")
        shutil.make_archive(base_output, 'zip', temp_project_dir)
        
        zip_output = base_output + ".zip"
        if os.path.exists(target_zip_path):
            os.remove(target_zip_path)
        os.rename(zip_output, target_zip_path)

        if os.path.exists(temp_project_dir):
            shutil.rmtree(temp_project_dir)
