class WebCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.canvasColor = '#FFFFFF';
        
        this.panOffset = { x: 0, y: 0 };
        this.zoomLevel = 1.0;
        this.isPanning = false;
        this.lastMousePos = { x: 0, y: 0 };

        this.stageWidth = 800;
        this.stageHeight = 450;

        this.resizeCanvas();
        this.bindEvents();
    }

    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
            this.drawStage([]);
        });

        this.canvas.addEventListener('mousedown', (e) => {
            if (e.button === 2) {
                this.isPanning = true;
                this.lastMousePos = { x: e.clientX, y: e.clientY };
            }
        });

        this.canvas.addEventListener('mousemove', (e) => {
            if (this.isPanning) {
                const deltaX = e.clientX - this.lastMousePos.x;
                const deltaY = e.clientY - this.lastMousePos.y;
                this.panOffset.x += deltaX;
                this.panOffset.y += deltaY;
                this.lastMousePos = { x: e.clientX, y: e.clientY };
                this.drawStage([]);
            }
        });

        window.addEventListener('mouseup', (e) => {
            if (e.button === 2) {
                this.isPanning = false;
            }
        });

        this.canvas.addEventListener('contextmenu', e => e.preventDefault());

        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            if (e.deltaY < 0) {
                this.zoomLevel *= 1.1;
            } else {
                this.zoomLevel /= 1.1;
            }
            this.drawStage([]);
        });
    }

    updateStageBg(hexColor) {
        this.canvasColor = hexColor;
    }

    drawStage(activeAssets) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.ctx.save();
        this.ctx.translate(this.canvas.width / 2 + this.panOffset.x, this.canvas.height / 2 + this.panOffset.y);
        this.ctx.scale(this.zoomLevel, this.zoomLevel);

        this.ctx.fillStyle = this.canvasColor;
        this.ctx.fillRect(-this.stageWidth / 2, -this.stageHeight / 2, this.stageWidth, this.stageHeight);

        this.renderToContext(this.ctx, activeAssets, this.stageWidth, this.stageHeight, true);

        this.ctx.strokeStyle = '#00A3FF';
        this.ctx.lineWidth = 1 / this.zoomLevel;
        this.ctx.strokeRect(-this.stageWidth / 2, -this.stageHeight / 2, this.stageWidth, this.stageHeight);

        this.ctx.restore();
    }

    renderToContext(context, assets, width, height, isWorkspace = false) {
        if (!assets) return;
        
        assets.forEach(obj => {
            if (obj instanceof VectorStroke) {
                if (obj.points.length < 2) return;
                context.beginPath();
                context.lineWidth = obj.size;
                context.strokeStyle = isWorkspace ? '#808080' : '#000000';
                context.lineCap = 'round';
                context.lineJoin = 'round';
                
                const startX = isWorkspace ? obj.points[0].x : (obj.points[0].x + width / 2);
                const startY = isWorkspace ? obj.points[0].y : (obj.points[0].y + height / 2);
                context.moveTo(startX, startY);

                for (let i = 1; i < obj.points.length; i++) {
                    const ptX = isWorkspace ? obj.points[i].x : (obj.points[i].x + width / 2);
                    const ptY = isWorkspace ? obj.points[i].y : (obj.points[i].y + height / 2);
                    context.lineTo(ptX, ptY);
                }
                context.stroke();
            }
        });
    }
}
