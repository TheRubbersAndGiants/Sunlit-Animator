class WebTimeline {
    constructor(appInstance) {
        this.app = appInstance;
        this.headersContainer = document.getElementById('layer-headers');
        this.tracksContainer = document.getElementById('timeline-tracks-container');
        this.initDOM();
    }

    initDOM() {
        this.renderHeaders();
        this.renderTracks();
    }

    renderHeaders() {
        this.headersContainer.innerHTML = '';
        for (let i = this.app.totalLayers - 1; i >= 0; i--) {
            const header = document.createElement('div');
            header.className = `layer-header ${i === this.app.currentLayer ? 'active' : 'inactive'}`;
            header.textContent = `Layer ${i + 1}`;
            header.addEventListener('click', () => {
                this.app.setFrameAndLayer(this.app.currentFrame, i);
            });
            this.headersContainer.appendChild(header);
        }
    }

    renderTracks() {
        this.tracksContainer.innerHTML = '';
        this.renderHeaders();

        for (let l = this.app.totalLayers - 1; l >= 0; l--) {
            const row = document.createElement('div');
            row.className = 'track-row';
            const layer = this.app.timelineModel.layers[l];

            for (let f = 0; f < this.app.totalFrames; f++) {
                const cell = document.createElement('div');
                cell.className = 'frame-cell';

                const kf = layer.keyframes[f];
                if (kf) {
                    if (kf.frameType === 'purple') cell.classList.add('tween-purple');
                    else if (kf.frameType === 'orange') cell.classList.add('tween-orange');
                    else if (kf.frameType === 'grey') cell.classList.add('frame-grey');
                }

                if (f === this.app.currentFrame && l === this.app.currentLayer) {
                    cell.classList.add('active-selection');
                }

                cell.addEventListener('click', () => {
                    this.app.setFrameAndLayer(f, l);
                });

                row.appendChild(cell);
            }
            this.tracksContainer.appendChild(row);
        }
    }
}
