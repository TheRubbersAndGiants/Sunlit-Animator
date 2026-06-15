from core.engine import ImportedBitmap, VectorStroke

class Keyframe:
    def __init__(self, frame_index, frame_type="grey"):
        self.frame_index = frame_index
        self.frame_type = frame_type
        self.objects = []
        self.ease_value = 0

class Layer:
    def __init__(self, name):
        self.name = name
        self.is_frame_by_frame = True
        self.keyframes = {}

    def get_or_create_frame(self, index):
        if index not in self.keyframes:
            self.keyframes[index] = Keyframe(index, "grey" if self.is_frame_by_frame else "purple")
        return self.keyframes[index]

class TimelineModel:
    def __init__(self, total_frames=60):
        self.total_frames = total_frames
        self.layers = [Layer("Layer 1"), Layer("Layer 2"), Layer("Layer 3")]

    def add_tween(self, layer_index, start_idx, end_idx, tween_type="purple"):
        layer = self.layers[layer_index]
        layer.is_frame_by_frame = False
        
        start_frame = layer.get_or_create_frame(start_idx)
        start_frame.frame_type = tween_type
        
        end_frame = layer.get_or_create_frame(end_idx)
        end_frame.frame_type = tween_type

    def convert_to_frame_by_frame(self, layer_index, start_idx, end_idx):
        layer = self.layers[layer_index]
        if layer.is_frame_by_frame:
            return

        for idx in range(start_idx, end_idx + 1):
            frame = layer.get_or_create_frame(idx)
            frame.frame_type = "grey"
            
        layer.is_frame_by_frame = True

    def evaluate_at_frame(self, layer_index, frame_index):
        layer = self.layers[layer_index]
        if frame_index in layer.keyframes:
            return layer.keyframes[frame_index].objects

        if layer.is_frame_by_frame:
            return []

        sorted_keys = sorted(layer.keyframes.keys())
        prev_key = None
        next_key = None

        for k in sorted_keys:
            if k <= frame_index:
                prev_key = k
            if k > frame_index and next_key is None:
                next_key = k
                break

        if prev_key is not None and next_key is not None:
            start_f = layer.keyframes[prev_key]
            end_f = layer.keyframes[next_key]
            
            if start_f.frame_type == "grey":
                return start_f.objects

            duration = next_key - prev_key
            progress = (frame_index - prev_key) / float(duration)
            
            return self.interpolate_frame_assets(start_f, end_f, progress)

        if prev_key is not None:
            return layer.keyframes[prev_key].objects

        return []

    def interpolate_frame_assets(self, start_frame, end_frame, progress):
        from core.engine import AnimationEngine
        interpolated_objects = []
        
        for idx, start_obj in enumerate(start_frame.objects):
            if idx >= len(end_frame.objects):
                continue
                
            end_obj = end_frame.objects[idx]
            if type(start_obj) != type(end_obj):
                continue

            if isinstance(start_obj, ImportedBitmap):
                new_bitmap = ImportedBitmap(start_obj.filepath, start_obj.name)
                new_bitmap.warp_grid = AnimationEngine.interpolate_grid(
                    start_obj.warp_grid, 
                    end_obj.warp_grid, 
                    progress, 
                    start_frame.ease_value
                )
                interpolated_objects.append(new_bitmap)
            elif isinstance(start_obj, VectorStroke):
                interpolated_objects.append(start_obj)

        return interpolated_objects
