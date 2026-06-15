class WebProperties {
    constructor(appInstance) {
        this.app = appInstance;
        
        this.colorPicker = document.getElementById('canvas-color-picker');
        this.objectList = document.getElementById('object-list');
        
        this.brushInput = document.getElementById('brush-size-input');
        this.brushSlider = document.getElementById('brush-size-slider');
        
        this.easeInput = document.getElementById('ease-val-input');
        this.easeSlider = document.getElementById('ease-val-slider');
        this.resetEaseBtn = document.getElementById('reset-ease-btn');

        this.newProjBtn = document.getElementById('menu-new-proj');
        this.saveProjBtn = document.getElementById('menu-save-proj');
        this.exportPngBtn = document.getElementById('menu-export-png');
        this.exportMovBtn = document.getElementById('menu-export-mov');
        this.importBitmapBtn = document.getElementById('menu-import-bitmap');
        this.hiddenUploader = document.getElementById('hidden-asset-uploader');

        this.bindEvents();
    }

    bindEvents() {
        this.colorPicker.addEventListener('input', (e) => {
            this.app.setCanvasColor(e.target.value);
        });

        this.brushInput.addEventListener('input', (e) => {
            let val = parseInt(e.target.value) || 1;
            val = Math.max(1, Math.min(200, val));
            this.brushSlider.value = val;
        });

        this.brushSlider.addEventListener('input', (e) => {
            this.brushInput.value = e.target.value;
        });

        this.easeInput.addEventListener('input', (e) => {
            let val = parseInt(e.target.value) || 0;
            val = Math.max(-1000, Math.min(1000, val));
            this.easeSlider.value = val;
            this.app.updateActiveKeyframeEase(val);
        });

        this.easeSlider.addEventListener('input', (e) => {
            this.easeInput.value = e.target.value;
            this.app.updateActiveKeyframeEase(parseInt(e.target.value));
        });

        this.resetEaseBtn.addEventListener('click', () => {
            this.easeInput.value = 0;
            this.easeSlider.value = 0;
            this.app.updateActiveKeyframeEase(0);
        });

        this.newProjBtn.addEventListener('click', () => {
            this.app.createNewProject();
        });

        this.saveProjBtn.addEventListener('click', () => {
            this.app.exportController.saveSunapProject();
        });

        this.exportPngBtn.addEventListener('click', () => {
            this.app.exportController.exportPngSequence();
        });

        this.exportMovBtn.addEventListener('click', () => {
            this.app.exportController.exportQuickTime();
        });

        this.importBitmapBtn.addEventListener('click', () => {
            this.hiddenUploader.click();
        });

        this.hiddenUploader.addEventListener('change', (e) => {
            if (e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = (event) => {
                    const bitmapAsset = new ImportedBitmap(event.target.result, file.name);
                    const currentLayerIdx = this.app.currentLayer;
                    const currentFrameIdx = this.app.currentFrame;
                    const activeKeyframe = this.app.timelineModel.layers[currentLayerIdx].getOrCreateFrame(currentFrameIdx);
                    activeKeyframe.objects.push(bitmapAsset);
                    this.app.updateGlobalUIState();
                };
                reader.readAsDataURL(file);
            }
        });
    }

    refreshObjectList(assets) {
        this.objectList.innerHTML = '';
        if (!assets) return;

        assets.forEach((obj) => {
            const li = document.createElement('li');
            li.textContent = obj.name;
            this.objectList.appendChild(li);
        });
    }

    setEasingDisplay(value) {
        this.easeInput.value = value;
        this.easeSlider.value = value;
    }
}
