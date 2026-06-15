class VectorStroke {
    constructor(size = 10) {
        this.name = "Brush Stroke";
        this.size = size;
        this.points = [];
    }
}

class ImportedBitmap {
    constructor(filepath, name = "Bitmap") {
        this.name = name;
        this.filepath = filepath;
        this.warpGrid = this.generateDefaultGrid();
    }

    generateDefaultGrid() {
        const grid = [];
        for (let row = 0; row < 5; row++) {
            const gridRow = [];
            for (let col = 0; col < 5; col++) {
                gridRow.push({
                    x: col * 0.25,
                    y: row * 0.25
                });
            }
            grid.push(gridRow);
        }
        return grid;
    }
}

class Keyframe {
    constructor(frameIndex, frameType = "grey") {
        this.frameIndex = frameIndex;
        this.frameType = frameType;
        this.objects = [];
        this.easeValue = 0;
    }
}

class Layer {
    constructor(name) {
        this.name = name;
        this.isFrameByFrame = true;
        this.keyframes = {};
    }

    getOrCreateFrame(index) {
        if (!this.keyframes[index]) {
            this.keyframes[index] = new Keyframe(index, this.isFrameByFrame ? "grey" : "purple");
        }
        return this.keyframes[index];
    }
}

class TimelineModel {
    constructor(totalFrames = 60, totalLayers = 3) {
        this.totalFrames = totalFrames;
        this.projectCanvasColor = "#FFFFFF";
        this.layers = [];
        for (let i = 0; i < totalLayers; i++) {
            this.layers.push(new Layer(`Layer ${i + 1}`));
        }
    }

    addTween(layerIndex, startIdx, endIdx, tweenType = "purple") {
        const layer = this.layers[layerIndex];
        layer.isFrameByFrame = false;
        
        const startFrame = layer.getOrCreateFrame(startIdx);
        startFrame.frameType = tweenType;
        
        const endFrame = layer.getOrCreateFrame(endIdx);
        endFrame.frameType = tweenType;
    }

    convertToFrameByFrame(layerIndex, startIdx, endIdx) {
        const layer = this.layers[layerIndex];
        if (layer.isFrameByFrame) return;

        for (let idx = startIdx; idx <= endIdx; idx++) {
            const frame = layer.getOrCreateFrame(idx);
            frame.frameType = "grey";
        }
        layer.isFrameByFrame = true;
    }

    interpolateValue(start, end, progress, easeValue) {
        if (easeValue !== 0) {
            const factor = easeValue / 1000.0;
            if (factor > 0) {
                progress = Math.pow(progress, 1.0 + factor * 2);
            } else {
                progress = 1.0 - Math.pow(1.0 - progress, 1.0 + Math.abs(factor) * 2);
            }
        }
        return start + (end - start) * progress;
    }

    interpolateGrid(startGrid, endGrid, progress, easeValue) {
        const newGrid = [];
        for (let r = 0; r < 5; r++) {
            const newRow = [];
            for (let c = 0; c < 5; c++) {
                const pStart = startGrid[r][c];
                const pEnd = endGrid[r][c];
                const interpX = this.interpolateValue(pStart.x, pEnd.x, progress, easeValue);
                const interpY = this.interpolateValue(pStart.y, pEnd.y, progress, easeValue);
                newRow.push({ x: interpX, y: interpY });
            }
            newGrid.push(newRow);
        }
        return newGrid;
    }

    evaluateAtFrame(layerIndex, frameIndex) {
        const layer = this.layers[layerIndex];
        if (layer.keyframes[frameIndex]) {
            return layer.keyframes[frameIndex].objects;
        }

        if (layer.isFrameByFrame) return [];

        const sortedKeys = Object.keys(layer.keyframes).map(Number).sort((a, b) => a - b);
        let prevKey = null;
        let nextKey = null;

        for (let k of sortedKeys) {
            if (k <= frameIndex) prevKey = k;
            if (k > frameIndex && nextKey === null) {
                nextKey = k;
                break;
            }
        }

        if (prevKey !== null && nextKey !== null) {
            const startF = layer.keyframes[prevKey];
            const endF = layer.keyframes[nextKey];
            
            if (startF.frameType === "grey") return startF.objects;

            const duration = nextKey - prevKey;
            const progress = (frameIndex - prevKey) / duration;
            
            return this.interpolateFrameAssets(startF, endF, progress);
        }

        if (prevKey !== null) return layer.keyframes[prevKey].objects;

        return [];
    }

    interpolateFrameAssets(startFrame, endFrame, progress) {
        const interpolatedObjects = [];
        const maxLen = Math.min(startFrame.objects.length, endFrame.objects.length);

        for (let i = 0; i < maxLen; i++) {
            const startObj = startFrame.objects[i];
            const endObj = endFrame.objects[i];

            if (startObj.constructor.name !== endObj.constructor.name) continue;

            if (startObj instanceof ImportedBitmap) {
                const newBitmap = new ImportedBitmap(startObj.filepath, startObj.name);
                newBitmap.warpGrid = this.interpolateGrid(startObj.warpGrid, endObj.warpGrid, progress, startFrame.easeValue);
                interpolatedObjects.append(newBitmap);
            } else if (startObj instanceof VectorStroke) {
                interpolatedObjects.push(startObj);
            }
        }
        return interpolatedObjects;
    }
}
