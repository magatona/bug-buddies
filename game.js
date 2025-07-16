class CurrencyManager {
    constructor() {
        this.coins = 0;
        this.gems = 0;
        this.earnRate = 1;
        this.lastEarnTime = Date.now();
        this.totalEarned = 0;
    }
    
    calculateEarnings(insects) {
        const now = Date.now();
        const deltaSeconds = (now - this.lastEarnTime) / 1000;
        
        if (deltaSeconds >= 1) {
            const earnings = insects.reduce((total, insect) => {
                return total + (insect.level * this.getSpeciesMultiplier(insect.type));
            }, 0) * this.earnRate;
            
            this.coins += Math.floor(earnings * deltaSeconds);
            this.totalEarned += Math.floor(earnings * deltaSeconds);
            this.lastEarnTime = now;
        }
    }
    
    getSpeciesMultiplier(type) {
        switch(type) {
            case 'beetle': return 1;
            case 'butterfly': return 1.5;
            case 'ladybug': return 2;
            case 'caterpillar': return 0.8;
            default: return 1;
        }
    }
    
    canAfford(cost) {
        return this.coins >= cost;
    }
    
    spend(amount) {
        if (this.canAfford(amount)) {
            this.coins -= amount;
            return true;
        }
        return false;
    }
}

class UnlockManager {
    constructor() {
        this.unlockedSpecies = ['beetle'];
        this.unlockedSlots = 1;
        this.speciesLevels = { 'beetle': 1 };
        this.unlockCosts = {
            species: {
                'butterfly': 100,
                'ladybug': 250,
                'caterpillar': 500,
                'dragonfly': 1000,
                'ant': 2000
            },
            slots: [0, 50, 150, 300, 500, 800]
        };
    }
    
    canUnlockSpecies(species) {
        return !this.unlockedSpecies.includes(species) && 
               this.unlockCosts.species[species] !== undefined;
    }
    
    unlockSpecies(species, currencyManager) {
        if (this.canUnlockSpecies(species)) {
            const cost = this.unlockCosts.species[species];
            if (currencyManager.spend(cost)) {
                this.unlockedSpecies.push(species);
                this.speciesLevels[species] = 1;
                return true;
            }
        }
        return false;
    }
    
    canUnlockSlot() {
        return this.unlockedSlots < this.unlockCosts.slots.length - 1;
    }
    
    unlockSlot(currencyManager) {
        if (this.canUnlockSlot()) {
            const cost = this.unlockCosts.slots[this.unlockedSlots + 1];
            if (currencyManager.spend(cost)) {
                this.unlockedSlots++;
                return true;
            }
        }
        return false;
    }
    
    getSpeciesLevel(species) {
        return this.speciesLevels[species] || 1;
    }
    
    setSpeciesLevel(species, level) {
        this.speciesLevels[species] = level;
    }
}

class CardManager {
    constructor(currencyManager, unlockManager) {
        this.currencyManager = currencyManager;
        this.unlockManager = unlockManager;
        this.speciesData = this.loadSpeciesData();
        this.cards = this.initializeCards();
        this.selectedCard = null;
        this.showDetailPanel = false;
        this.cardWidth = 80;
        this.cardHeight = 60;
        this.cardSpacing = 5;
    }
    
    loadSpeciesData() {
        return {
            "insects": {
                "beetle": {
                    "name_jp": "カブトムシ",
                    "name_en": "Beetle",
                    "description": "のっそりと歩く茶色の昆虫。力強く、安定した収益を生み出します。",
                    "base_cost": 120,
                    "upgrade_costs": [120, 300, 720, 1800, 4000, 8000, 15000, 25000, 40000, 60000],
                    "max_level": 10,
                    "earnings_multiplier": 1.0
                },
                "butterfly": {
                    "name_jp": "蝶々",
                    "name_en": "Butterfly", 
                    "description": "ひらひらと舞う美しい昆虫。中程度の収益と魅力的な動きが特徴です。",
                    "base_cost": 300,
                    "upgrade_costs": [300, 750, 1800, 4500, 10000, 20000, 35000, 55000, 80000, 120000],
                    "max_level": 10,
                    "earnings_multiplier": 1.5
                },
                "ladybug": {
                    "name_jp": "てんとう虫",
                    "name_en": "Ladybug",
                    "description": "ちょこちょこと素早く動く赤い昆虫。高い収益率を誇ります。",
                    "base_cost": 720,
                    "upgrade_costs": [720, 1800, 4320, 10800, 24000, 48000, 84000, 132000, 192000, 288000],
                    "max_level": 10,
                    "earnings_multiplier": 2.0
                },
                "caterpillar": {
                    "name_jp": "イモムシ",
                    "name_en": "Caterpillar",
                    "description": "ゆっくりと這う緑の昆虫。低コストで始められる初心者向けです。",
                    "base_cost": 1800,
                    "upgrade_costs": [1800, 4500, 10800, 27000, 60000, 120000, 210000, 330000, 480000, 720000],
                    "max_level": 10,
                    "earnings_multiplier": 0.8
                },
                "dragonfly": {
                    "name_jp": "トンボ",
                    "name_en": "Dragonfly",
                    "description": "空中を優雅に舞う昆虫。高速移動と優秀な収益性を持ちます。",
                    "base_cost": 4000,
                    "upgrade_costs": [4000, 10000, 24000, 60000, 133000, 266000, 466000, 733000, 1066000, 1600000],
                    "max_level": 10,
                    "earnings_multiplier": 2.5
                },
                "ant": {
                    "name_jp": "アリ",
                    "name_en": "Ant",
                    "description": "組織的に行動する働き者の昆虫。集団効果で収益が向上します。",
                    "base_cost": 6000,
                    "upgrade_costs": [6000, 15000, 36000, 90000, 200000, 400000, 700000, 1100000, 1600000, 2400000],
                    "max_level": 10,
                    "earnings_multiplier": 1.8
                }
            }
        };
    }
    
    initializeCards() {
        const speciesOrder = ['beetle', 'butterfly', 'ladybug', 'caterpillar', 'dragonfly', 'ant'];
        return speciesOrder.map(species => ({
            id: species,
            data: this.speciesData.insects[species],
            x: 0, y: 0,
            state: this.getCardState(species)
        }));
    }
    
    getCardState(species) {
        if (this.unlockManager.unlockedSpecies.includes(species)) {
            return 'owned';
        } else if (this.currencyManager.canAfford(this.getSpeciesCost(species))) {
            return 'available';
        } else {
            return 'locked';
        }
    }
    
    getSpeciesCost(species) {
        return this.speciesData.insects[species]?.base_cost || 0;
    }
    
    getUpgradeCost(species, currentLevel) {
        const data = this.speciesData.insects[species];
        if (!data || currentLevel >= data.max_level) return 0;
        return data.upgrade_costs[currentLevel] || 0;
    }
    
    handleCardClick(cardId) {
        const card = this.cards.find(c => c.id === cardId);
        if (!card) return;
        
        if (card.state === 'available') {
            this.purchaseSpecies(cardId);
        } else if (card.state === 'owned') {
            this.showSpeciesDetail(cardId);
        }
    }
    
    purchaseSpecies(species) {
        const cost = this.getSpeciesCost(species);
        if (this.currencyManager.spend(cost)) {
            this.unlockManager.unlockedSpecies.push(species);
            this.unlockManager.speciesLevels[species] = 1;
            this.updateCardStates();
            console.log(`Purchased ${species} for ${cost} coins!`);
            return true;
        }
        return false;
    }
    
    showSpeciesDetail(species) {
        this.selectedCard = this.cards.find(c => c.id === species);
        this.showDetailPanel = true;
    }
    
    hideDetailPanel() {
        this.showDetailPanel = false;
        this.selectedCard = null;
    }
    
    upgradeSpecies(speciesId) {
        const currentLevel = this.unlockManager.getSpeciesLevel(speciesId);
        const upgradeCost = this.getUpgradeCost(speciesId, currentLevel);
        
        if (upgradeCost > 0 && this.currencyManager.canAfford(upgradeCost)) {
            this.currencyManager.spend(upgradeCost);
            this.unlockManager.setSpeciesLevel(speciesId, currentLevel + 1);
            console.log(`Upgraded ${speciesId} to level ${currentLevel + 1} for ${upgradeCost} coins!`);
            return true;
        }
        return false;
    }
    
    updateCardStates() {
        this.cards.forEach(card => {
            card.state = this.getCardState(card.id);
        });
    }
    
    getCardAtPosition(x, y) {
        return this.cards.find(card => 
            x >= card.x && x <= card.x + this.cardWidth &&
            y >= card.y && y <= card.y + this.cardHeight
        );
    }
    
    layoutCards() {
        const startX = 10;
        const startY = 15;
        const maxCardsPerRow = Math.floor((window.innerWidth - 20) / (this.cardWidth + this.cardSpacing));
        
        this.cards.forEach((card, index) => {
            const row = Math.floor(index / maxCardsPerRow);
            const col = index % maxCardsPerRow;
            
            card.x = startX + col * (this.cardWidth + this.cardSpacing);
            card.y = startY + row * (this.cardHeight + this.cardSpacing);
        });
    }
    
    drawSpeciesIcon(ctx, speciesData, x, y, species) {
        const size = 20;
        const halfSize = size / 2;
        
        ctx.save();
        ctx.translate(x, y);
        
        switch(species) {
            case 'beetle':
                ctx.fillStyle = '#8B4513';
                ctx.beginPath();
                ctx.ellipse(0, 0, halfSize * 0.8, halfSize * 0.6, 0, 0, Math.PI * 2);
                ctx.fill();
                break;
            case 'butterfly':
                ctx.fillStyle = '#FF69B4';
                ctx.beginPath();
                ctx.ellipse(-halfSize * 0.3, -halfSize * 0.3, halfSize * 0.4, halfSize * 0.3, 0, 0, Math.PI * 2);
                ctx.ellipse(halfSize * 0.3, -halfSize * 0.3, halfSize * 0.4, halfSize * 0.3, 0, 0, Math.PI * 2);
                ctx.fill();
                break;
            case 'ladybug':
                ctx.fillStyle = '#FF0000';
                ctx.beginPath();
                ctx.ellipse(0, 0, halfSize * 0.7, halfSize * 0.5, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.arc(-halfSize * 0.2, -halfSize * 0.1, halfSize * 0.1, 0, Math.PI * 2);
                ctx.arc(halfSize * 0.2, -halfSize * 0.1, halfSize * 0.1, 0, Math.PI * 2);
                ctx.fill();
                break;
            case 'caterpillar':
                ctx.fillStyle = '#32CD32';
                for (let i = 0; i < 3; i++) {
                    const segX = (i - 1) * halfSize * 0.4;
                    ctx.beginPath();
                    ctx.arc(segX, 0, halfSize * 0.3, 0, Math.PI * 2);
                    ctx.fill();
                }
                break;
            case 'dragonfly':
                ctx.fillStyle = '#006400';
                ctx.fillRect(-halfSize * 0.1, -halfSize, halfSize * 0.2, size);
                ctx.fillStyle = '#C8C8FF';
                ctx.beginPath();
                ctx.ellipse(-halfSize * 0.4, -halfSize * 0.2, halfSize * 0.3, halfSize * 0.1, 0, 0, Math.PI * 2);
                ctx.ellipse(halfSize * 0.4, -halfSize * 0.2, halfSize * 0.3, halfSize * 0.1, 0, 0, Math.PI * 2);
                ctx.fill();
                break;
            case 'ant':
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.arc(-halfSize * 0.3, 0, halfSize * 0.2, 0, Math.PI * 2);
                ctx.arc(0, 0, halfSize * 0.25, 0, Math.PI * 2);
                ctx.arc(halfSize * 0.3, 0, halfSize * 0.2, 0, Math.PI * 2);
                ctx.fill();
                break;
        }
        
        ctx.restore();
    }
    
    renderCard(ctx, card) {
        const { x, y } = card;
        const { cardWidth, cardHeight } = this;
        
        const bgColor = {
            'available': 'rgba(0, 255, 0, 0.8)',
            'locked': 'rgba(100, 100, 100, 0.6)',
            'owned': 'rgba(0, 100, 255, 0.8)'
        }[card.state];
        
        ctx.fillStyle = bgColor;
        ctx.fillRect(x, y, cardWidth, cardHeight);
        
        ctx.strokeStyle = card.state === 'available' ? '#00FF00' : card.state === 'owned' ? '#0066FF' : '#666666';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, cardWidth, cardHeight);
        
        this.drawSpeciesIcon(ctx, card.data, x + cardWidth/2, y + 20, card.id);
        
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(card.data.name_jp, x + cardWidth/2, y + cardHeight - 15);
        
        if (card.state !== 'owned') {
            ctx.fillText(`${card.data.base_cost}💰`, x + cardWidth/2, y + cardHeight - 5);
        } else {
            const level = this.unlockManager.getSpeciesLevel(card.id);
            ctx.fillText(`Lv.${level}`, x + cardWidth/2, y + cardHeight - 5);
        }
    }
    
    wrapText(ctx, text, x, y, maxWidth, lineHeight) {
        const words = text.split('');
        let line = '';
        let currentY = y;
        
        for (let i = 0; i < words.length; i++) {
            const testLine = line + words[i];
            const metrics = ctx.measureText(testLine);
            const testWidth = metrics.width;
            
            if (testWidth > maxWidth && i > 0) {
                ctx.fillText(line, x, currentY);
                line = words[i];
                currentY += lineHeight;
            } else {
                line = testLine;
            }
        }
        ctx.fillText(line, x, currentY);
    }
    
    renderUpgradeButton(ctx, x, y) {
        if (!this.selectedCard) return;
        
        const currentLevel = this.unlockManager.getSpeciesLevel(this.selectedCard.id);
        const upgradeCost = this.getUpgradeCost(this.selectedCard.id, currentLevel);
        const canUpgrade = upgradeCost > 0 && this.currencyManager.canAfford(upgradeCost);
        
        ctx.fillStyle = canUpgrade ? 'rgba(0, 255, 0, 0.8)' : 'rgba(150, 150, 150, 0.8)';
        ctx.fillRect(x, y, 70, 20);
        
        ctx.strokeStyle = canUpgrade ? '#00FF00' : '#999999';
        ctx.lineWidth = 1;
        ctx.strokeRect(x, y, 70, 20);
        
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        
        if (currentLevel >= this.selectedCard.data.max_level) {
            ctx.fillText('最大レベル', x + 35, y + 14);
        } else {
            ctx.fillText(`強化 ${upgradeCost}💰`, x + 35, y + 14);
        }
        
        this.upgradeButtonBounds = { x, y, width: 70, height: 20 };
    }
    
    renderDetailPanel(ctx) {
        if (!this.selectedCard) return;
        
        const panelWidth = 300;
        const panelHeight = 80;
        const panelX = (ctx.canvas.width - panelWidth) / 2;
        const panelY = 10;
        
        ctx.fillStyle = 'rgba(240, 230, 200, 0.95)';
        ctx.fillRect(panelX, panelY, panelWidth, panelHeight);
        
        ctx.strokeStyle = '#8B4513';
        ctx.lineWidth = 2;
        ctx.strokeRect(panelX, panelY, panelWidth, panelHeight);
        
        const card = this.selectedCard;
        const level = this.unlockManager.getSpeciesLevel(card.id);
        
        ctx.fillStyle = '#000000';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`${card.data.name_jp} Lv.${level}`, panelX + 10, panelY + 20);
        
        ctx.font = '10px Arial';
        this.wrapText(ctx, card.data.description, panelX + 10, panelY + 35, panelWidth - 100, 12);
        
        if (card.state === 'owned') {
            this.renderUpgradeButton(ctx, panelX + panelWidth - 80, panelY + panelHeight - 25);
        }
        
        ctx.fillStyle = 'rgba(255, 0, 0, 0.8)';
        ctx.fillRect(panelX + panelWidth - 20, panelY + 5, 15, 15);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('×', panelX + panelWidth - 12, panelY + 15);
        
        this.closeBounds = { x: panelX + panelWidth - 20, y: panelY + 5, width: 15, height: 15 };
    }
    
    handleDetailPanelClick(x, y) {
        if (this.closeBounds && 
            x >= this.closeBounds.x && x <= this.closeBounds.x + this.closeBounds.width &&
            y >= this.closeBounds.y && y <= this.closeBounds.y + this.closeBounds.height) {
            this.hideDetailPanel();
            return true;
        }
        
        if (this.upgradeButtonBounds && 
            x >= this.upgradeButtonBounds.x && x <= this.upgradeButtonBounds.x + this.upgradeButtonBounds.width &&
            y >= this.upgradeButtonBounds.y && y <= this.upgradeButtonBounds.y + this.upgradeButtonBounds.height) {
            if (this.selectedCard) {
                this.upgradeSpecies(this.selectedCard.id);
            }
            return true;
        }
        
        return false;
    }
    
    renderCards(ctx) {
        this.updateCardStates();
        this.layoutCards();
        this.cards.forEach(card => this.renderCard(ctx, card));
        if (this.showDetailPanel) {
            this.renderDetailPanel(ctx);
        }
    }
}

class BugBuddies {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.insects = [];
        this.food = [];
        this.environment = [];
        this.lastTime = 0;
        
        this.currencyManager = new CurrencyManager();
        this.unlockManager = new UnlockManager();
        this.cardManager = new CardManager(this.currencyManager, this.unlockManager);
        this.buttons = this.initializeButtons();
        
        this.loadGameState();
        
        this.setupCanvas();
        this.setupEventListeners();
        this.createInitialInsects();
        this.createEnvironment();
        this.gameLoop();
        
        setInterval(() => this.saveGameState(), 10000);
    }
    
    setupCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = 100;
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            if (this.cardManager.showDetailPanel) {
                if (this.cardManager.handleDetailPanelClick(x, y)) {
                    return;
                }
            }
            
            const clickedCard = this.cardManager.getCardAtPosition(x, y);
            if (clickedCard) {
                this.cardManager.handleCardClick(clickedCard.id);
                return;
            }
            
            const clickedButton = this.buttons.find(button => 
                x >= button.x && x <= button.x + button.width &&
                y >= button.y && y <= button.y + button.height
            );
            
            if (clickedButton && this.isButtonEnabled(clickedButton)) {
                clickedButton.action();
            } else {
                this.dropFood(x, y);
            }
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
            this.buttons = this.initializeButtons();
            this.cardManager.layoutCards();
        });
        
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case '1':
                    this.unlockSpecies('butterfly');
                    break;
                case '2':
                    this.unlockSpecies('ladybug');
                    break;
                case '3':
                    this.unlockSpecies('caterpillar');
                    break;
                case '4':
                    this.unlockSpecies('dragonfly');
                    break;
                case '5':
                    this.unlockSpecies('ant');
                    break;
                case 's':
                    this.unlockSlot();
                    break;
                case 'c':
                    this.currencyManager.coins += 100;
                    console.log(`Added 100 coins. Total: ${this.currencyManager.coins}`);
                    break;
            }
        });
    }
    
    initializeButtons() {
        const buttonWidth = 80;
        const buttonHeight = 25;
        const buttonSpacing = 10;
        const startX = 20;
        const startY = 80; // Position in visible lower area of canvas
        
        
        return [
            { x: startX, y: startY, width: buttonWidth, height: buttonHeight, 
              label: 'Butterfly', action: () => this.unlockSpecies('butterfly'), 
              cost: this.unlockManager.unlockCosts.species.butterfly, species: 'butterfly' },
            { x: startX + (buttonWidth + buttonSpacing) * 1, y: startY, width: buttonWidth, height: buttonHeight,
              label: 'Ladybug', action: () => this.unlockSpecies('ladybug'),
              cost: this.unlockManager.unlockCosts.species.ladybug, species: 'ladybug' },
            { x: startX + (buttonWidth + buttonSpacing) * 2, y: startY, width: buttonWidth, height: buttonHeight,
              label: 'Caterpillar', action: () => this.unlockSpecies('caterpillar'),
              cost: this.unlockManager.unlockCosts.species.caterpillar, species: 'caterpillar' },
            { x: startX + (buttonWidth + buttonSpacing) * 3, y: startY, width: buttonWidth, height: buttonHeight,
              label: 'Dragonfly', action: () => this.unlockSpecies('dragonfly'),
              cost: this.unlockManager.unlockCosts.species.dragonfly, species: 'dragonfly' },
            { x: startX + (buttonWidth + buttonSpacing) * 4, y: startY, width: buttonWidth, height: buttonHeight,
              label: 'Ant', action: () => this.unlockSpecies('ant'),
              cost: this.unlockManager.unlockCosts.species.ant, species: 'ant' },
            { x: startX + (buttonWidth + buttonSpacing) * 5, y: startY, width: buttonWidth, height: buttonHeight,
              label: 'Add Slot', action: () => this.unlockSlot(),
              cost: () => this.unlockManager.unlockCosts.slots[this.unlockManager.unlockedSlots + 1] || 0, isSlot: true },
            { x: startX + (buttonWidth + buttonSpacing) * 6, y: startY, width: buttonWidth, height: buttonHeight,
              label: '+100 Coins', action: () => { this.currencyManager.coins += 100; console.log(`Added 100 coins. Total: ${this.currencyManager.coins}`); },
              cost: 0, isTest: true }
        ];
    }
    
    isButtonEnabled(button) {
        if (button.isTest) return true;
        
        if (button.species) {
            return this.unlockManager.canUnlockSpecies(button.species) && 
                   this.currencyManager.canAfford(button.cost);
        } else if (button.isSlot) {
            const cost = typeof button.cost === 'function' ? button.cost() : button.cost;
            return this.unlockManager.canUnlockSlot() && 
                   this.currencyManager.canAfford(cost);
        }
        
        return false;
    }
    
    renderButtons() {
        this.buttons.forEach((button, index) => {
            const enabled = this.isButtonEnabled(button);
            const cost = typeof button.cost === 'function' ? button.cost() : button.cost;
            
            this.ctx.fillStyle = enabled ? 'rgba(0, 255, 0, 0.9)' : 'rgba(255, 0, 0, 0.9)';
            this.ctx.fillRect(button.x, button.y, button.width, button.height);
            
            this.ctx.strokeStyle = enabled ? '#00FF00' : '#FF0000';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(button.x, button.y, button.width, button.height);
            
            this.ctx.fillStyle = '#FFFFFF';
            this.ctx.font = '12px Arial';
            this.ctx.textAlign = 'center';
            
            this.ctx.fillText(button.label, button.x + button.width/2, button.y + 15);
            
            if (!button.isTest && cost > 0) {
                this.ctx.fillText(`${cost}💰`, button.x + button.width/2, button.y + 25);
            }
        });
        
        this.ctx.textAlign = 'left';
    }
    
    createInitialInsects() {
        const availableSpecies = this.unlockManager.unlockedSpecies;
        const maxSlots = this.unlockManager.unlockedSlots;
        const positions = [
            { x: this.canvas.width * 0.2, y: 70 },
            { x: this.canvas.width * 0.4, y: 50 },
            { x: this.canvas.width * 0.6, y: 80 },
            { x: this.canvas.width * 0.8, y: 60 }
        ];
        
        for (let i = 0; i < Math.min(maxSlots, availableSpecies.length); i++) {
            const type = availableSpecies[i % availableSpecies.length];
            const position = positions[i % positions.length];
            const insect = new Insect(type, position.x, position.y);
            this.insects.push(insect);
        }
    }

    createEnvironment() {
        for (let i = 0; i < 8; i++) {
            this.environment.push({
                type: 'grass',
                x: Math.random() * this.canvas.width,
                y: 85 + Math.random() * 10
            });
        }
        
        for (let i = 0; i < 3; i++) {
            this.environment.push({
                type: 'flower',
                x: Math.random() * this.canvas.width,
                y: 75 + Math.random() * 15
            });
        }
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
        
        this.currencyManager.calculateEarnings(this.insects);
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
        
        this.renderEnvironment();
        
        this.food.forEach(food => {
            food.render(this.ctx);
        });
        
        this.insects.forEach(insect => {
            insect.render(this.ctx);
        });
        
        this.renderUI();
    }

    renderEnvironment() {
        this.environment.forEach(element => {
            if (element.type === 'grass') {
                this.drawGrass(this.ctx, element.x, element.y);
            } else if (element.type === 'flower') {
                this.drawFlower(this.ctx, element.x, element.y);
            }
        });
    }

    drawGrass(ctx, x, y) {
        ctx.save();
        ctx.translate(x, y);
        
        ctx.fillStyle = '#228B22';
        ctx.beginPath();
        ctx.moveTo(-2, 0);
        ctx.lineTo(-1, -6);
        ctx.lineTo(0, 0);
        ctx.fill();
        
        ctx.fillStyle = '#32CD32';
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(1, -7);
        ctx.lineTo(2, 0);
        ctx.fill();
        
        ctx.fillStyle = '#228B22';
        ctx.beginPath();
        ctx.moveTo(2, 0);
        ctx.lineTo(3, -5);
        ctx.lineTo(4, 0);
        ctx.fill();
        
        ctx.restore();
    }

    drawFlower(ctx, x, y) {
        ctx.save();
        ctx.translate(x, y);
        
        const petalCount = 5;
        const petalRadius = 3;
        
        ctx.fillStyle = '#FFB6C1';
        for (let i = 0; i < petalCount; i++) {
            const angle = (i * 2 * Math.PI) / petalCount;
            const petalX = Math.cos(angle) * 4;
            const petalY = Math.sin(angle) * 4;
            
            ctx.beginPath();
            ctx.ellipse(petalX, petalY, petalRadius, petalRadius * 0.6, angle, 0, Math.PI * 2);
            ctx.fill();
        }
        
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(0, 0, 2, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
    
    renderUI() {
        this.ctx.save();
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(10, 10, 200, 60);
        
        this.ctx.fillStyle = '#FFD700';
        this.ctx.font = '16px Arial';
        this.ctx.fillText(`💰 Coins: ${this.currencyManager.coins}`, 20, 30);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '12px Arial';
        this.ctx.fillText(`Earn Rate: ${this.currencyManager.earnRate}/sec`, 20, 45);
        this.ctx.fillText(`Total Earned: ${this.currencyManager.totalEarned}`, 20, 60);
        
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(this.canvas.width - 220, 10, 210, 80);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '14px Arial';
        this.ctx.fillText('Unlocked Species:', this.canvas.width - 210, 30);
        
        this.ctx.font = '12px Arial';
        let yOffset = 45;
        this.unlockManager.unlockedSpecies.forEach(species => {
            this.ctx.fillText(`• ${species}`, this.canvas.width - 200, yOffset);
            yOffset += 15;
        });
        
        this.ctx.fillText(`Slots: ${this.unlockManager.unlockedSlots}`, this.canvas.width - 200, yOffset + 5);
        
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        this.ctx.fillRect(10, this.canvas.height - 50, this.canvas.width - 20, 40);
        
        this.ctx.fillStyle = '#FFFFFF';
        this.ctx.font = '10px Arial';
        this.ctx.fillText('Click cards to purchase/upgrade • Click empty area to feed insects • Right-click for menu', 15, this.canvas.height - 5);
        
        this.cardManager.renderCards(this.ctx);
        
        this.ctx.restore();
    }
    
    unlockSpecies(species) {
        if (this.unlockManager.unlockSpecies(species, this.currencyManager)) {
            console.log(`Unlocked ${species}!`);
            if (this.insects.length < this.unlockManager.unlockedSlots) {
                const position = this.getAvailablePosition();
                const newInsect = new Insect(species, position.x, position.y);
                this.insects.push(newInsect);
            }
            return true;
        }
        return false;
    }
    
    unlockSlot() {
        if (this.unlockManager.unlockSlot(this.currencyManager)) {
            console.log(`Unlocked new slot! Total slots: ${this.unlockManager.unlockedSlots}`);
            const availableSpecies = this.unlockManager.unlockedSpecies;
            if (availableSpecies.length > 0) {
                const randomSpecies = availableSpecies[Math.floor(Math.random() * availableSpecies.length)];
                const position = this.getAvailablePosition();
                const newInsect = new Insect(randomSpecies, position.x, position.y);
                this.insects.push(newInsect);
            }
            return true;
        }
        return false;
    }
    
    getAvailablePosition() {
        const positions = [
            { x: this.canvas.width * 0.2, y: 70 },
            { x: this.canvas.width * 0.4, y: 50 },
            { x: this.canvas.width * 0.6, y: 80 },
            { x: this.canvas.width * 0.8, y: 60 },
            { x: this.canvas.width * 0.1, y: 65 },
            { x: this.canvas.width * 0.9, y: 75 }
        ];
        
        return positions[this.insects.length % positions.length];
    }
    
    saveGameState() {
        const gameState = {
            currency: {
                coins: this.currencyManager.coins,
                gems: this.currencyManager.gems,
                totalEarned: this.currencyManager.totalEarned
            },
            unlocks: {
                unlockedSpecies: this.unlockManager.unlockedSpecies,
                unlockedSlots: this.unlockManager.unlockedSlots,
                speciesLevels: this.unlockManager.speciesLevels
            },
            insects: this.insects.map(insect => ({
                type: insect.type,
                x: insect.x,
                y: insect.y,
                level: insect.level,
                experience: insect.experience
            }))
        };
        
        localStorage.setItem('bugBuddiesGameState', JSON.stringify(gameState));
    }
    
    loadGameState() {
        const savedState = localStorage.getItem('bugBuddiesGameState');
        if (savedState) {
            try {
                const gameState = JSON.parse(savedState);
                
                if (gameState.currency) {
                    this.currencyManager.coins = gameState.currency.coins || 0;
                    this.currencyManager.gems = gameState.currency.gems || 0;
                    this.currencyManager.totalEarned = gameState.currency.totalEarned || 0;
                }
                
                if (gameState.unlocks) {
                    this.unlockManager.unlockedSpecies = gameState.unlocks.unlockedSpecies || ['beetle'];
                    this.unlockManager.unlockedSlots = gameState.unlocks.unlockedSlots || 1;
                    this.unlockManager.speciesLevels = gameState.unlocks.speciesLevels || { 'beetle': 1 };
                }
                
                console.log('Game state loaded successfully');
            } catch (error) {
                console.error('Failed to load game state:', error);
            }
        }
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
        this.speed = this.getSpeciesSpeed();
        this.direction = Math.random() > 0.5 ? 1 : -1;
        this.movementPattern = this.getMovementPattern();
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

    getSpeciesSpeed() {
        switch(this.type) {
            case 'beetle': return 0.02;
            case 'butterfly': return 0.025;
            case 'ladybug': return 0.03;
            case 'caterpillar': return 0.015;
            default: return 0.02;
        }
    }

    getMovementPattern() {
        switch(this.type) {
            case 'butterfly': return 'flutter';
            case 'ladybug': return 'quick';
            case 'caterpillar': return 'crawl';
            default: return 'walk';
        }
    }

    applyMovementPattern(deltaTime) {
        if (this.movementPattern === 'flutter' && !this.targetX) {
            this.y += Math.sin(Date.now() * 0.003) * 0.5;
            this.y = Math.max(30, Math.min(90, this.y));
        } else if (this.movementPattern === 'quick' && Math.random() < 0.002) {
            this.speed *= 2;
            setTimeout(() => { this.speed = this.getSpeciesSpeed(); }, 500);
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
        
        this.applyMovementPattern(deltaTime);
        
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
window.game = game;
