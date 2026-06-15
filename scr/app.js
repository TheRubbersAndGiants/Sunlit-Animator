class SunlitAnimatorApp {
    constructor() {
        this.currentFrame = 0;
        this.currentLayer = 0;
        this.totalFrames = 60;
        this.totalLayers = 3;

        this.timelineModel = new TimelineModel(this.totalFrames, this.totalLayers);
        
        this.initModules();
        this.bindGlobalEvents();
        this.updateGlobalUIState();
    }

    initModules() {
        this.canvasController = new WebCanvas('stage-canvas');
        this.timelineController = new WebTimeline(this);
        this.propertiesController = new WebProperties(this);
        this.exportController = new WebExport(this);
    }

    bindGlobalEvents() {
        window.addEventListener('keydown', (e) => {
            if (document.activeElement.tagName === 'INPUT') return;

            switch (e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.changeFrame(-1);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.changeFrame(1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.changeLayer(-1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.changeLayer(1);
                    break;
                case '9':
                    e.preventDefault();
                    this.timelineModel.addTween(this.currentLayer, this.currentFrame, this.currentFrame + 10, 'purple');
                    this.updateGlobalUIState();
                    break;
                case '0':
                    e.preventDefault();
                    this.timelineModel.convertToFrameByFrame(this.currentLayer, this.currentFrame, this.currentFrame + 10);
                    this.updateGlobalUIState();
                    break;
            }
        });
    }

    changeFrame(delta) {
        const target = this.currentFrame + delta;
        if (target >= 0 && target < this.totalFrames) {
            this.currentFrame = target;
            this.updateGlobalUIState();
        }
    }

    changeLayer(delta) {
        const target = this.currentLayer + delta;
        if (target >= 0 && target < this.totalLayers) {
            this.currentLayer = target;
            this.updateGlobalUIState();
        }
    }

    setFrameAndLayer(frameIdx, layerIdx) {
        this.currentFrame = frameIdx;
        this.currentLayer = layerIdx;
        this.updateGlobalUIState();
    }

    updateGlobalUIState() {
        this.timelineController.renderTracks();
        
        const activeAssets = this.timelineModel.evaluateAtFrame(this.currentLayer, this.currentFrame);
        this.propertiesController.refreshObjectList(activeAssets);
        
        const layer = this.timelineModel.layers[this.currentLayer];
        const currentKf = layer.keyframes[this.currentFrame];
        if (currentKf) {
            this.propertiesController.setEasingDisplay(currentKf.easeValue);
        } else {
            this.propertiesController.setEasingDisplay(0);
        }

        this.canvasController.drawStage(activeAssets);
    }

    setCanvasColor(hexColor) {
        this.timelineModel.projectCanvasColor = hexColor;
        this.canvasController.updateStageBg(hexColor);
    }

    updateActiveKeyframeEase(value) {
        const layer = this.timelineModel.layers[this.currentLayer];
        const kf = layer.getOrCreateFrame(this.currentFrame);
        kf.easeValue = value;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.App = new SunlitAnimatorApp();
});
