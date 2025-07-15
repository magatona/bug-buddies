class AssetManager {
    constructor() {
        this.assets = {
            characters: {},
            animations: {},
            ui: {}
        };
        this.manifest = null;
        this.loadedAssets = new Map();
        this.loadingPromises = new Map();
        this.fallbackEnabled = true;
        
        console.log('🎨 AssetManager initialized');
    }
    
    async initialize() {
        try {
            await this.loadManifest();
            await this.preloadCriticalAssets();
            console.log('✅ AssetManager ready');
            return true;
        } catch (error) {
            console.warn('⚠️ AssetManager initialization failed, using fallback mode:', error);
            this.fallbackEnabled = true;
            return false;
        }
    }
    
    async loadManifest() {
        try {
            const response = await fetch('assets/manifest.json');
            if (!response.ok) {
                throw new Error(`Failed to load manifest: ${response.status}`);
            }
            
            this.manifest = await response.json();
            console.log(`📋 Loaded manifest with ${this.manifest.total_assets} assets`);
            
            this.assets.characters = this.manifest.characters || {};
            this.assets.animations = this.manifest.animations || {};
            this.assets.ui = this.manifest.ui_elements || [];
            
        } catch (error) {
            console.error('❌ Failed to load asset manifest:', error);
            throw error;
        }
    }
    
    async preloadCriticalAssets() {
        const criticalAssets = [
            { type: 'character', insect: 'beetle', variant: 'idle' },
            { type: 'character', insect: 'butterfly', variant: 'idle' },
            { type: 'character', insect: 'ladybug', variant: 'idle' },
            { type: 'character', insect: 'caterpillar', variant: 'idle' }
        ];
        
        console.log('🔄 Preloading critical assets...');
        
        const preloadPromises = criticalAssets.map(async (asset) => {
            try {
                await this.getCharacterAsset(asset.insect, asset.variant);
            } catch (error) {
                console.warn(`⚠️ Failed to preload ${asset.insect} ${asset.variant}:`, error);
            }
        });
        
        await Promise.allSettled(preloadPromises);
        console.log('✅ Critical assets preloaded');
    }
    
    async getCharacterAsset(insectType, variant = 'idle') {
        const assetKey = `character_${insectType}_${variant}`;
        
        if (this.loadedAssets.has(assetKey)) {
            return this.loadedAssets.get(assetKey);
        }
        
        if (this.loadingPromises.has(assetKey)) {
            return this.loadingPromises.get(assetKey);
        }
        
        const loadPromise = this.loadCharacterAsset(insectType, variant);
        this.loadingPromises.set(assetKey, loadPromise);
        
        try {
            const asset = await loadPromise;
            this.loadedAssets.set(assetKey, asset);
            this.loadingPromises.delete(assetKey);
            return asset;
        } catch (error) {
            this.loadingPromises.delete(assetKey);
            throw error;
        }
    }
    
    async loadCharacterAsset(insectType, variant) {
        try {
            const characterAssets = this.assets.characters[insectType];
            if (!characterAssets || characterAssets.length === 0) {
                throw new Error(`No assets found for ${insectType}`);
            }
            
            let assetFile = characterAssets.find(file => file.includes(variant));
            if (!assetFile) {
                assetFile = characterAssets.find(file => file.includes('idle'));
                if (!assetFile) {
                    assetFile = characterAssets[0];
                }
            }
            
            const assetPath = `assets/characters/${insectType}/${assetFile}`;
            
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = () => {
                    console.log(`✅ Loaded character asset: ${assetPath}`);
                    resolve(img);
                };
                img.onerror = () => {
                    reject(new Error(`Failed to load image: ${assetPath}`));
                };
                img.src = assetPath;
            });
            
        } catch (error) {
            console.error(`❌ Failed to load character asset ${insectType}/${variant}:`, error);
            throw error;
        }
    }
    
    async getAnimation(insectType, animationType = 'idle') {
        const animationKey = `animation_${insectType}_${animationType}`;
        
        if (this.loadedAssets.has(animationKey)) {
            return this.loadedAssets.get(animationKey);
        }
        
        if (this.loadingPromises.has(animationKey)) {
            return this.loadingPromises.get(animationKey);
        }
        
        const loadPromise = this.loadAnimation(insectType, animationType);
        this.loadingPromises.set(animationKey, loadPromise);
        
        try {
            const animation = await loadPromise;
            this.loadedAssets.set(animationKey, animation);
            this.loadingPromises.delete(animationKey);
            return animation;
        } catch (error) {
            this.loadingPromises.delete(animationKey);
            throw error;
        }
    }
    
    async loadAnimation(insectType, animationType) {
        try {
            const animationAssets = this.assets.animations[insectType];
            if (!animationAssets || animationAssets.length === 0) {
                throw new Error(`No animations found for ${insectType}`);
            }
            
            let animationFile = animationAssets.find(file => file.includes(animationType));
            if (!animationFile) {
                animationFile = animationAssets.find(file => file.includes('idle'));
                if (!animationFile) {
                    animationFile = animationAssets[0];
                }
            }
            
            const animationPath = `assets/animations/${insectType}/${animationFile}`;
            
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = () => {
                    console.log(`🎬 Loaded animation: ${animationPath}`);
                    resolve({
                        image: img,
                        path: animationPath,
                        type: animationType
                    });
                };
                img.onerror = () => {
                    reject(new Error(`Failed to load animation: ${animationPath}`));
                };
                img.src = animationPath;
            });
            
        } catch (error) {
            console.error(`❌ Failed to load animation ${insectType}/${animationType}:`, error);
            throw error;
        }
    }
    
    async getUIAsset(elementName) {
        const assetKey = `ui_${elementName}`;
        
        if (this.loadedAssets.has(assetKey)) {
            return this.loadedAssets.get(assetKey);
        }
        
        try {
            const uiFile = this.assets.ui.find(file => file.includes(elementName));
            if (!uiFile) {
                throw new Error(`UI asset not found: ${elementName}`);
            }
            
            const assetPath = `assets/ui/${uiFile}`;
            
            const asset = await new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = () => resolve(img);
                img.onerror = () => reject(new Error(`Failed to load UI asset: ${assetPath}`));
                img.src = assetPath;
            });
            
            this.loadedAssets.set(assetKey, asset);
            console.log(`🎮 Loaded UI asset: ${assetPath}`);
            return asset;
            
        } catch (error) {
            console.error(`❌ Failed to load UI asset ${elementName}:`, error);
            throw error;
        }
    }
    
    isAssetAvailable(insectType, variant = 'idle') {
        return this.assets.characters[insectType] && 
               this.assets.characters[insectType].length > 0;
    }
    
    isAnimationAvailable(insectType, animationType = 'idle') {
        return this.assets.animations[insectType] && 
               this.assets.animations[insectType].length > 0;
    }
    
    getAvailableCharacters() {
        return Object.keys(this.assets.characters);
    }
    
    getAvailableAnimations(insectType) {
        return this.assets.animations[insectType] || [];
    }
    
    clearCache() {
        this.loadedAssets.clear();
        this.loadingPromises.clear();
        console.log('🧹 Asset cache cleared');
    }
    
    getStats() {
        return {
            manifestLoaded: !!this.manifest,
            totalAssets: this.manifest?.total_assets || 0,
            loadedAssets: this.loadedAssets.size,
            availableCharacters: Object.keys(this.assets.characters).length,
            availableAnimations: Object.keys(this.assets.animations).length,
            fallbackEnabled: this.fallbackEnabled
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = AssetManager;
}
