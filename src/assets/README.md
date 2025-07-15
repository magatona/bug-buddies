# 🎨 AssetManager Documentation

The AssetManager is a comprehensive asset loading and management system for Bug Buddies that seamlessly integrates AI-generated pixel art with the existing game engine.

## 🚀 Quick Start

```javascript
// Initialize AssetManager
const assetManager = new AssetManager();
await assetManager.initialize();

// Load character asset
const beetleSprite = await assetManager.getCharacterAsset('beetle', 'idle');

// Load animation
const walkingAnimation = await assetManager.getAnimation('beetle', 'walking');

// Load UI element
const foodIcon = await assetManager.getUIAsset('food_pellet');
```

## 📋 API Reference

### Constructor

```javascript
const assetManager = new AssetManager();
```

Creates a new AssetManager instance with empty asset cache.

### Methods

#### `initialize()`
```javascript
await assetManager.initialize();
```
- Loads the asset manifest
- Preloads critical assets
- Returns: `Promise<boolean>` - Success status

#### `getCharacterAsset(insectType, variant)`
```javascript
const sprite = await assetManager.getCharacterAsset('beetle', 'idle');
```
- **insectType**: `'beetle'`, `'butterfly'`, `'ladybug'`, `'caterpillar'`
- **variant**: `'idle'`, `'walk_1'`, `'walk_2'`, `'level_2'`, `'level_3'`
- Returns: `Promise<HTMLImageElement>`

#### `getAnimation(insectType, animationType)`
```javascript
const animation = await assetManager.getAnimation('butterfly', 'flying');
```
- **insectType**: Insect type identifier
- **animationType**: `'walking'`, `'flying'`, `'crawling'`, `'idle'`
- Returns: `Promise<{image: HTMLImageElement, path: string, type: string}>`

#### `getUIAsset(elementName)`
```javascript
const icon = await assetManager.getUIAsset('heart_icon');
```
- **elementName**: UI element identifier
- Returns: `Promise<HTMLImageElement>`

#### `isAssetAvailable(insectType, variant)`
```javascript
const available = assetManager.isAssetAvailable('beetle', 'idle');
```
- Returns: `boolean` - Whether asset exists in manifest

#### `getStats()`
```javascript
const stats = assetManager.getStats();
console.log(stats);
// {
//   manifestLoaded: true,
//   totalAssets: 45,
//   loadedAssets: 12,
//   availableCharacters: 4,
//   availableAnimations: 4,
//   fallbackEnabled: true
// }
```

## 🎮 Game Integration

### Insect Class Integration

```javascript
class Insect {
    constructor(type, x, y) {
        // ... existing code ...
        this.currentAsset = null;
        this.useAssets = false;
        
        if (window.assetManager) {
            this.loadAssets();
        }
    }
    
    async loadAssets() {
        try {
            if (window.assetManager.isAssetAvailable(this.type)) {
                this.currentAsset = await window.assetManager.getCharacterAsset(this.type, 'idle');
                this.useAssets = true;
            }
        } catch (error) {
            console.warn(`Failed to load assets for ${this.type}:`, error);
            this.useAssets = false;
        }
    }
    
    render(ctx) {
        if (this.useAssets && this.currentAsset) {
            this.drawAssetSprite(ctx);
        } else {
            this.drawInsect(ctx);  // Fallback to programmatic drawing
        }
    }
}
```

### Fallback System

The AssetManager provides seamless fallback to programmatic drawing:

```javascript
drawAssetSprite(ctx) {
    try {
        ctx.drawImage(this.currentAsset, -16, -16, 32, 32);
    } catch (error) {
        console.warn('Asset drawing failed, using fallback');
        this.useAssets = false;
        this.drawInsect(ctx);  // Fallback to programmatic drawing
    }
}
```

## 📁 Asset Structure

### Manifest Format

```json
{
  "version": "1.0.0",
  "generated_at": "2025-07-14T10:30:00Z",
  "characters": {
    "beetle": ["beetle_idle.png", "beetle_walk_1.png", "beetle_walk_2.png"],
    "butterfly": ["butterfly_idle.png", "butterfly_fly_1.png", "butterfly_fly_2.png"],
    "ladybug": ["ladybug_idle.png", "ladybug_walk_1.png"],
    "caterpillar": ["caterpillar_idle.png", "caterpillar_crawl_1.png"]
  },
  "animations": {
    "beetle": ["beetle_walking.gif", "beetle_idle.gif"],
    "butterfly": ["butterfly_flying.gif", "butterfly_idle.gif"]
  },
  "ui_elements": ["food_pellet.png", "sparkle_effect.png", "heart_icon.png"],
  "total_assets": 15
}
```

### Directory Structure

```
assets/
├── characters/
│   ├── beetle/
│   │   ├── beetle_idle.png
│   │   ├── beetle_walk_1.png
│   │   └── beetle_walk_2.png
│   ├── butterfly/
│   │   ├── butterfly_idle.png
│   │   ├── butterfly_fly_1.png
│   │   └── butterfly_fly_2.png
│   └── ...
├── animations/
│   ├── beetle/
│   │   ├── beetle_walking.gif
│   │   └── beetle_idle.gif
│   └── ...
├── ui/
│   ├── food_pellet.png
│   ├── sparkle_effect.png
│   └── heart_icon.png
└── manifest.json
```

## 🔧 Configuration

### Preloading Configuration

Critical assets are preloaded for performance:

```javascript
const criticalAssets = [
    { type: 'character', insect: 'beetle', variant: 'idle' },
    { type: 'character', insect: 'butterfly', variant: 'idle' },
    { type: 'character', insect: 'ladybug', variant: 'idle' },
    { type: 'character', insect: 'caterpillar', variant: 'idle' }
];
```

### Caching Strategy

- **Lazy Loading**: Assets loaded on first request
- **Memory Caching**: Loaded assets cached in memory
- **Promise Deduplication**: Multiple requests for same asset share promise
- **Cache Clearing**: Manual cache clearing for memory management

## 🚨 Error Handling

### Common Error Scenarios

1. **Manifest Loading Failure**
   ```javascript
   // AssetManager falls back to programmatic drawing
   this.fallbackEnabled = true;
   ```

2. **Individual Asset Loading Failure**
   ```javascript
   // Specific asset request fails, game continues
   console.warn('Failed to load beetle_idle.png, using fallback');
   ```

3. **Network Issues**
   ```javascript
   // Automatic retry with exponential backoff
   await this.retryAssetLoad(assetPath, 3);
   ```

### Debug Mode

Enable debug logging:

```javascript
// In browser console
localStorage.setItem('assetManagerDebug', 'true');
location.reload();
```

## 📊 Performance Optimization

### Best Practices

1. **Preload Critical Assets**: Load essential sprites during initialization
2. **Lazy Load Variants**: Load level variations and animations on-demand
3. **Cache Management**: Clear cache periodically to prevent memory leaks
4. **Asset Compression**: Use optimized PNG/GIF formats
5. **Fallback Strategy**: Always provide programmatic drawing fallback

### Performance Metrics

```javascript
const stats = assetManager.getStats();
console.log(`Cache efficiency: ${stats.loadedAssets}/${stats.totalAssets}`);
```

## 🔄 Asset Updates

### Hot Reloading

Assets can be updated without game restart:

```javascript
// Clear cache and reload manifest
assetManager.clearCache();
await assetManager.initialize();

// Reload specific insect assets
insects.forEach(insect => insect.loadAssets());
```

### Version Management

The manifest includes version information for cache invalidation:

```javascript
if (manifest.version !== cachedVersion) {
    assetManager.clearCache();
    // Reload all assets
}
```

## 🧪 Testing

### Unit Tests

```javascript
// Test asset availability
assert(assetManager.isAssetAvailable('beetle', 'idle'));

// Test loading
const sprite = await assetManager.getCharacterAsset('beetle', 'idle');
assert(sprite instanceof HTMLImageElement);

// Test fallback
assetManager.fallbackEnabled = true;
// Game should continue working
```

### Integration Tests

```javascript
// Test with missing manifest
// Test with corrupted assets
// Test network failure scenarios
// Test memory usage under load
```

## 🔗 Related Documentation

- [Asset Generation Pipeline](../scripts/README.md)
- [Game Integration Guide](../README.md#game-integration)
- [Troubleshooting Guide](../README.md#troubleshooting)
