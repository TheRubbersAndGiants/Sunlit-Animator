class WebExport {
    constructor(appInstance) {
        this.app = appInstance;
    }

    async triggerDownload(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async exportPngSequence() {
        const zip = new JSZip();
        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = 1920;
        exportCanvas.height = 1080;
        const ctx = exportCanvas.getContext('2d');

        for (let f = 0; f < this.app.totalFrames; f++) {
            ctx.fillStyle = this.app.timelineModel.projectCanvasColor;
            ctx.fillRect(0, 0, 1920, 1080);

            for (let l = 0; l < this.app.totalLayers; l++) {
                const assets = this.app.timelineModel.evaluateAtFrame(l, f);
                this.app.canvasController.renderToContext(ctx, assets, 1920, 1080);
            }

            const frameBlob = await new Promise(resolve => exportCanvas.toBlob(resolve, 'image/png'));
            const frameName = `frame_${String(f).padStart(4, '0')}.png`;
            zip.file(frameName, frameBlob);
        }

        const zipBlob = await zip.generateAsync({ type: 'blob' });
        this.triggerDownload(zipBlob, 'animation_sequence.zip');
    }

    exportQuickTime() {
        const streamCanvas = document.createElement('canvas');
        streamCanvas.width = 1920;
        streamCanvas.height = 1080;
        const ctx = streamCanvas.getContext('2d');

        const stream = streamCanvas.captureStream(24);
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm;codecs=vp9' });
        const chunks = [];

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) chunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
            const videoBlob = new Blob(chunks, { type: 'video/quicktime' });
            this.triggerDownload(videoBlob, 'animation.mov');
        };

        let currentFrame = 0;
        mediaRecorder.start();

        const recordInterval = setInterval(() => {
            if (currentFrame >= this.app.totalFrames) {
                clearInterval(recordInterval);
                mediaRecorder.stop();
                return;
            }

            ctx.fillStyle = this.app.timelineModel.projectCanvasColor;
            ctx.fillRect(0, 0, 1920, 1080);

            for (let l = 0; l < this.app.totalLayers; l++) {
                const assets = this.app.timelineModel.evaluateAtFrame(l, currentFrame);
                this.app.canvasController.renderToContext(ctx, assets, 1920, 1080);
            }

            currentFrame++;
        }, 1000 / 24);
    }

    async saveSunapProject() {
        const zip = new JSZip();
        
        const projectData = {
            canvasColor: this.app.timelineModel.projectCanvasColor,
            totalFrames: this.app.totalFrames,
            layers: []
        };

        this.app.timelineModel.layers.forEach(layer => {
            const layerDict = {
                name: layer.name,
                isFrameByFrame: layer.isFrameByFrame,
                keyframes: {}
            };

            Object.keys(layer.keyframes).forEach(idx => {
                const kf = layer.keyframes[idx];
                const kfDict = {
                    frameType: kf.frameType,
                    easeValue: kf.easeValue,
                    objects: []
                };

                kf.objects.forEach(obj => {
                    if (obj instanceof ImportedBitmap) {
                        kfDict.objects.push({
                            type: 'bitmap',
                            name: obj.name,
                            filepath: obj.filepath,
                            warpGrid: obj.warpGrid
                        });
                    } else if (obj instanceof VectorStroke) {
                        kfDict.objects.push({
                            type: 'vector_stroke',
                            name: obj.name,
                            size: obj.size,
                            points: obj.points
                        });
                    }
                });

                layerDict.keyframes[idx] = kfDict;
            });

            projectData.layers.push(layerDict);
        });

        zip.file('project.json', JSON.stringify(projectData, null, 4));
        const sunapBlob = await zip.generateAsync({ type: 'blob' });
        this.triggerDownload(sunapBlob, 'project.sunap');
    }
}
