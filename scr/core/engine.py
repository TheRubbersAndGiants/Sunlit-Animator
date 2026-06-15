import math

class VectorStroke:
    def __init__(self, size=10):
        self.name = "Brush Stroke"
        self.size = size
        self.points = []

class ImportedBitmap:
    def __init__(self, filepath, name="Bitmap"):
        self.name = name
        self.filepath = filepath
        self.warp_grid = self.generate_default_grid()

    def generate_default_grid(self):
        grid = []
        for row in range(5):
            grid_row = []
            for col in range(5):
                grid_row.append({
                    "x": col * 0.25,
                    "y": row * 0.25
                })
            grid.append(grid_row)
        return grid

class AnimationEngine:
    @staticmethod
    def interpolate_value(start, end, progress, ease_value):
        if ease_value != 0:
            factor = ease_value / 1000.0
            if factor > 0:
                progress = math.pow(progress, 1.0 + factor * 2)
            else:
                progress = 1.0 - math.pow(1.0 - progress, 1.0 + abs(factor) * 2)
        return start + (end - start) * progress

    @staticmethod
    def interpolate_grid(start_grid, end_grid, progress, ease_value):
        new_grid = []
        for r in range(5):
            new_row = []
            for c in range(5):
                p_start = start_grid[r][c]
                p_end = end_grid[r][c]
                interp_x = AnimationEngine.interpolate_value(p_start["x"], p_end["x"], progress, ease_value)
                interp_y = AnimationEngine.interpolate_value(p_start["y"], p_end["y"], progress, ease_value)
                new_row.append({"x": interp_x, "y": interp_y})
            new_grid.append(new_row)
        return new_grid
