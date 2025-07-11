class BugBuddies {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.insects = [];
        this.food = [];
        this.lastTime = 0;
        
        this.setupCanvas();
        this.setupEventListeners();
        this.createInitialInsect();
        this.gameLoop();
    }
    
    setupCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = 100;
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('click', (e) => {
            this.dropFood(e.clientX, e.clientY);
        });
        
        this.canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showContextMenu(e.clientX, e.clientY);
        });
        
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.context-menu')) {
                this.hideContextMenu();
            }
        });
        
        window.addEventListener('resize', () => {
            this.setupCanvas();
        });
    }
    
    createInitialInsect() {
        const beetle = new Insect('beetle', this.canvas.width / 2, 70);
        this.insects.push(beetle);
    }
    
    dropFood(x, y) {
        const food = new Food(x, y);
        this.food.push(food);
        
        this.insects.forEach(insect => {
            insect.setTarget(x, y);
        });
    }
    
    showContextMenu(x, y) {
        const menu = document.getElementById('contextMenu');
        menu.style.left = x + 'px';
        menu.style.top = y + 'px';
        menu.style.display = 'block';
    }
    
    hideContextMenu() {
        document.getElementById('contextMenu').style.display = 'none';
    }
    
    update(deltaTime) {
        this.insects.forEach(insect => {
            insect.update(deltaTime);
        });
        
        this.food = this.food.filter(food => {
            food.update(deltaTime);
            return !food.consumed;
        });
        
        this.checkCollisions();
    }
    
    checkCollisions() {
        this.insects.forEach(insect => {
            this.food.forEach(food => {
                if (!food.consumed && this.distance(insect.x, insect.y, food.x, food.y) < 20) {
                    food.consume();
                    insect.feed();
                }
            });
        });
    }
    
    distance(x1, y1, x2, y2) {
        return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    }
    
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.food.forEach(food => {
            food.render(this.ctx);
        });
        
        this.insects.forEach(insect => {
            insect.render(this.ctx);
        });
    }
    
    gameLoop(currentTime = 0) {
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame((time) => this.gameLoop(time));
    }
}

class Insect {
    constructor(type, x, y) {
        this.type = type;
        this.x = x;
        this.y = y;
        this.targetX = null;
        this.targetY = null;
        this.speed = 0.02;
        this.direction = Math.random() > 0.5 ? 1 : -1;
        this.animationFrame = 0;
        this.animationTime = 0;
        this.restTime = 0;
        this.isResting = false;
        this.level = 1;
        this.experience = 0;
        this.size = 32;
        
        this.colors = this.getColors();
    }
    
    getColors() {
        switch(this.type) {
            case 'beetle':
                return { primary: '#8B4513', secondary: '#654321' };
            case 'butterfly':
                return { primary: '#FF69B4', secondary: '#FFB6C1' };
            case 'ladybug':
                return { primary: '#FF0000', secondary: '#000000' };
            case 'caterpillar':
                return { primary: '#32CD32', secondary: '#228B22' };
            default:
                return { primary: '#8B4513', secondary: '#654321' };
        }
    }
    
    setTarget(x, y) {
        this.targetX = x;
        this.targetY = y;
        this.isResting = false;
    }
    
    update(deltaTime) {
        this.animationTime += deltaTime;
        
        if (this.isResting) {
            this.restTime += deltaTime;
            if (this.restTime > 1000) {
                this.isResting = false;
                this.restTime = 0;
            }
            return;
        }
        
        if (this.targetX !== null && this.targetY !== null) {
            const dx = this.targetX - this.x;
            const dy = this.targetY - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > 5) {
                this.x += (dx / distance) * this.speed * deltaTime;
                this.y += (dy / distance) * this.speed * deltaTime;
                this.direction = dx > 0 ? 1 : -1;
            } else {
                this.targetX = null;
                this.targetY = null;
                this.isResting = true;
            }
        } else {
            this.x += this.direction * this.speed * deltaTime;
            
            if (this.x < 0 || this.x > window.innerWidth) {
                this.direction *= -1;
                this.isResting = true;
            }
            
            if (Math.random() < 0.001) {
                this.isResting = true;
            }
        }
        
        if (this.animationTime > 500) {
            this.animationFrame = (this.animationFrame + 1) % 2;
            this.animationTime = 0;
        }
        
        this.experience += deltaTime * 0.001;
        if (this.experience >= this.level * 100) {
            this.levelUp();
        }
    }
    
    levelUp() {
        this.level++;
        this.experience = 0;
        this.size = Math.min(48, 32 + this.level * 2);
        console.log(`${this.type} leveled up to ${this.level}!`);
    }
    
    feed() {
        this.experience += 50;
        console.log(`${this.type} ate food! Experience: ${this.experience}`);
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        
        if (this.direction < 0) {
            ctx.scale(-1, 1);
        }
        
        this.drawInsect(ctx);
        
        ctx.restore();
        
        this.drawLevelIndicator(ctx);
    }
    
    drawInsect(ctx) {
        const size = this.size;
        const halfSize = size / 2;
        
        switch(this.type) {
            case 'beetle':
                this.drawBeetle(ctx, size);
                break;
            case 'butterfly':
                this.drawButterfly(ctx, size);
                break;
            case 'ladybug':
                this.drawLadybug(ctx, size);
                break;
            case 'caterpillar':
                this.drawCaterpillar(ctx, size);
                break;
        }
    }
    
    drawBeetle(ctx, size) {
        const halfSize = size / 2;
        
        ctx.fillStyle = this.colors.primary;
        ctx.beginPath();
        ctx.ellipse(0, 0, halfSize * 0.8, halfSize * 0.6, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = this.colors.secondary;
        ctx.beginPath();
        ctx.ellipse(-halfSize * 0.3, -halfSize * 0.2, halfSize * 0.2, halfSize * 0.15, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(-halfSize * 0.6, halfSize * 0.2);
        ctx.lineTo(-halfSize * 0.8, halfSize * 0.4);
        ctx.moveTo(-halfSize * 0.4, halfSize * 0.3);
        ctx.lineTo(-halfSize * 0.6, halfSize * 0.5);
        ctx.moveTo(-halfSize * 0.2, halfSize * 0.4);
        ctx.lineTo(-halfSize * 0.4, halfSize * 0.6);
        ctx.stroke();
    }
    
    drawButterfly(ctx, size) {
        const halfSize = size / 2;
        
        ctx.fillStyle = this.colors.primary;
        ctx.beginPath();
        ctx.ellipse(-halfSize * 0.3, -halfSize * 0.3, halfSize * 0.4, halfSize * 0.3, 0, 0, Math.PI * 2);
        ctx.ellipse(halfSize * 0.3, -halfSize * 0.3, halfSize * 0.4, halfSize * 0.3, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = this.colors.secondary;
        ctx.beginPath();
        ctx.ellipse(-halfSize * 0.2, halfSize * 0.2, halfSize * 0.3, halfSize * 0.2, 0, 0, Math.PI * 2);
        ctx.ellipse(halfSize * 0.2, halfSize * 0.2, halfSize * 0.3, halfSize * 0.2, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, -halfSize * 0.5);
        ctx.lineTo(0, halfSize * 0.5);
        ctx.stroke();
    }
    
    drawLadybug(ctx, size) {
        const halfSize = size / 2;
        
        ctx.fillStyle = this.colors.primary;
        ctx.beginPath();
        ctx.ellipse(0, 0, halfSize * 0.7, halfSize * 0.5, 0, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = this.colors.secondary;
        ctx.beginPath();
        ctx.arc(-halfSize * 0.2, -halfSize * 0.1, halfSize * 0.1, 0, Math.PI * 2);
        ctx.arc(halfSize * 0.2, -halfSize * 0.1, halfSize * 0.1, 0, Math.PI * 2);
        ctx.arc(0, halfSize * 0.1, halfSize * 0.08, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.ellipse(0, -halfSize * 0.3, halfSize * 0.3, halfSize * 0.2, 0, 0, Math.PI * 2);
        ctx.fill();
    }
    
    drawCaterpillar(ctx, size) {
        const halfSize = size / 2;
        const segments = 4;
        
        for (let i = 0; i < segments; i++) {
            const x = (i - segments/2 + 0.5) * halfSize * 0.4;
            const segmentSize = halfSize * 0.3 * (1 - i * 0.05);
            
            ctx.fillStyle = i === 0 ? this.colors.secondary : this.colors.primary;
            ctx.beginPath();
            ctx.arc(x, 0, segmentSize, 0, Math.PI * 2);
            ctx.fill();
        }
        
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(-halfSize * 0.4, -halfSize * 0.1, 2, 0, Math.PI * 2);
        ctx.arc(-halfSize * 0.3, -halfSize * 0.1, 2, 0, Math.PI * 2);
        ctx.fill();
    }
    
    drawLevelIndicator(ctx) {
        if (this.level > 1) {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.font = '10px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`Lv.${this.level}`, this.x, this.y - this.size/2 - 5);
        }
    }
}

class Food {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.consumed = false;
        this.life = 10000;
        this.maxLife = 10000;
    }
    
    update(deltaTime) {
        this.life -= deltaTime;
        if (this.life <= 0) {
            this.consumed = true;
        }
    }
    
    consume() {
        this.consumed = true;
    }
    
    render(ctx) {
        if (this.consumed) return;
        
        const alpha = this.life / this.maxLife;
        ctx.save();
        ctx.globalAlpha = alpha;
        
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 4, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#FFA500';
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
}

function openSettings() {
    console.log('Settings opened');
    document.getElementById('contextMenu').style.display = 'none';
}

function openEncyclopedia() {
    console.log('Encyclopedia opened');
    document.getElementById('contextMenu').style.display = 'none';
}

function exitApp() {
    if (typeof require !== 'undefined') {
        const { remote } = require('electron');
        remote.app.quit();
    }
    document.getElementById('contextMenu').style.display = 'none';
}

const game = new BugBuddies();
