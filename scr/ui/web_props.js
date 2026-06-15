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
