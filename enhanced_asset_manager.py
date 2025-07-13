from PIL import Image, ImageDraw
import os
import math
import json

class AssetManager:
    """Enhanced asset manager for Bug Buddies game with animation support"""
    
    def __init__(self):
        self.asset_config = {
            'insects': {
                'beetle': {
                    'name_jp': 'カブトムシ',
                    'colors': {'primary': (139, 69, 19), 'secondary': (101, 67, 33)},
                    'speed': 'slow',
                    'animation_duration': 600,
                    'movement_style': 'walk'
                },
                'butterfly': {
                    'name_jp': '蝶々',
                    'colors': {'primary': (255, 105, 180), 'secondary': (255, 182, 193)},
                    'speed': 'medium',
                    'animation_duration': 400,
                    'movement_style': 'flutter'
                },
                'ladybug': {
                    'name_jp': 'てんとう虫',
                    'colors': {'primary': (255, 0, 0), 'secondary': (0, 0, 0)},
                    'speed': 'fast',
                    'animation_duration': 300,
                    'movement_style': 'quick'
                },
                'caterpillar': {
                    'name_jp': 'イモムシ',
                    'colors': {'primary': (50, 205, 50), 'secondary': (34, 139, 34)},
                    'speed': 'very_slow',
                    'animation_duration': 800,
                    'movement_style': 'crawl'
                },
                'dragonfly': {
                    'name_jp': 'トンボ',
                    'colors': {'primary': (0, 100, 0), 'secondary': (200, 200, 255)},
                    'speed': 'fast',
                    'animation_duration': 350,
                    'movement_style': 'hover'
                },
                'ant': {
                    'name_jp': 'アリ',
                    'colors': {'primary': (0, 0, 0), 'secondary': (50, 50, 50)},
                    'speed': 'medium',
                    'animation_duration': 450,
                    'movement_style': 'march'
                }
            }
        }
    
    def create_enhanced_beetle_frames(self):
        """Enhanced beetle animation with more detailed features"""
        frames = []
        
        for frame in range(2):
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            colors = self.asset_config['insects']['beetle']['colors']
            draw.ellipse([8, 12, 24, 20], fill=colors['primary'])
            draw.ellipse([10, 13, 22, 19], fill=colors['secondary'])
            
            draw.ellipse([10, 8, 14, 12], fill=colors['secondary'])
            draw.ellipse([18, 8, 22, 12], fill=colors['secondary'])
            
            draw.ellipse([11, 9, 13, 11], fill=(0, 0, 0))
            draw.ellipse([19, 9, 21, 11], fill=(0, 0, 0))
            draw.ellipse([11.5, 9.5, 12, 10], fill=(255, 255, 255))
            draw.ellipse([19.5, 9.5, 20, 10], fill=(255, 255, 255))
            
            leg_offset = 1.5 if frame == 1 else 0
            for i in range(3):
                y_offset = 14 + i * 2
                draw.line([(8, y_offset), (6 - leg_offset, y_offset + 2 + leg_offset)], fill=(0, 0, 0), width=2)
                draw.line([(24, y_offset), (26 + leg_offset, y_offset + 2 + leg_offset)], fill=(0, 0, 0), width=2)
            
            draw.polygon([(16, 8), (15, 4), (17, 4)], fill=colors['secondary'])
            draw.line([(16, 8), (16, 4)], fill=(0, 0, 0), width=1)
            
            draw.ellipse([9, 13, 15, 19], outline=(80, 50, 15), width=1)
            draw.ellipse([17, 13, 23, 19], outline=(80, 50, 15), width=1)
            
            frames.append(img)
        
        return frames
    
    def create_enhanced_butterfly_frames(self):
        """Enhanced butterfly with more realistic wing patterns"""
        frames = []
        
        for frame in range(2):
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            colors = self.asset_config['insects']['butterfly']['colors']
            
            draw.line([(16, 6), (16, 22)], fill=(0, 0, 0), width=2)
            
            draw.ellipse([14, 6, 18, 8], fill=(0, 0, 0))
            draw.line([(15, 6), (13, 4)], fill=(0, 0, 0), width=1)
            draw.line([(17, 6), (19, 4)], fill=(0, 0, 0), width=1)
            draw.ellipse([12, 3, 14, 5], fill=(0, 0, 0))
            draw.ellipse([18, 3, 20, 5], fill=(0, 0, 0))
            
            wing_offset = 3 if frame == 1 else 0
            wing_rotation = 5 if frame == 1 else -5
            
            draw.ellipse([8, 8 - wing_offset, 18, 12 - wing_offset], fill=colors['primary'])
            draw.ellipse([14, 8 - wing_offset, 24, 12 - wing_offset], fill=colors['primary'])
            
            draw.ellipse([10, 9 - wing_offset, 14, 11 - wing_offset], fill=(255, 255, 0))
            draw.ellipse([18, 9 - wing_offset, 22, 11 - wing_offset], fill=(255, 255, 0))
            draw.ellipse([11, 9.5 - wing_offset, 13, 10.5 - wing_offset], fill=(255, 0, 0))
            draw.ellipse([19, 9.5 - wing_offset, 21, 10.5 - wing_offset], fill=(255, 0, 0))
            
            draw.ellipse([10, 16 + wing_offset, 16, 20 + wing_offset], fill=colors['secondary'])
            draw.ellipse([16, 16 + wing_offset, 22, 20 + wing_offset], fill=colors['secondary'])
            
            frames.append(img)
        
        return frames
    
    def create_food_sprites(self):
        """Create various food items for insects"""
        food_items = {}
        
        img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([4, 6, 12, 14], fill=(255, 215, 0))
        draw.ellipse([5, 7, 11, 13], fill=(255, 255, 0))
        food_items['honey'] = img
        
        img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([2, 4, 14, 12], fill=(34, 139, 34))
        draw.line([(8, 4), (8, 12)], fill=(0, 100, 0), width=1)
        food_items['leaf'] = img
        
        img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for angle in [0, 72, 144, 216, 288]:
            x = 8 + 3 * math.cos(math.radians(angle))
            y = 8 + 3 * math.sin(math.radians(angle))
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 105, 180))
        draw.ellipse([6, 6, 10, 10], fill=(255, 255, 0))
        food_items['nectar'] = img
        
        return food_items
    
    def create_ui_elements(self):
        """Create enhanced UI elements"""
        ui_elements = {}
        
        img = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([2, 2, 22, 22], fill=(255, 215, 0))
        draw.ellipse([4, 4, 20, 20], fill=(255, 255, 0))
        draw.text((8, 8), "¥", fill=(255, 165, 0))
        ui_elements['coin'] = img
        
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = 12
            else:
                radius = 6
            x = 16 + radius * math.cos(angle - math.pi/2)
            y = 16 + radius * math.sin(angle - math.pi/2)
            points.append((x, y))
        draw.polygon(points, fill=(255, 255, 0))
        ui_elements['levelup'] = img
        
        return ui_elements
    
    def generate_all_assets(self):
        """Generate all game assets"""
        print("🎨 Generating enhanced Bug Buddies assets...")
        
        os.makedirs('assets/insects/enhanced', exist_ok=True)
        os.makedirs('assets/food', exist_ok=True)
        os.makedirs('assets/ui/enhanced', exist_ok=True)
        
        beetle_frames = self.create_enhanced_beetle_frames()
        self.create_animated_gif(beetle_frames, 'assets/insects/enhanced/beetle_enhanced.gif', 
                               self.asset_config['insects']['beetle']['animation_duration'])
        
        butterfly_frames = self.create_enhanced_butterfly_frames()
        self.create_animated_gif(butterfly_frames, 'assets/insects/enhanced/butterfly_enhanced.gif',
                               self.asset_config['insects']['butterfly']['animation_duration'])
        
        food_items = self.create_food_sprites()
        for name, img in food_items.items():
            img.save(f'assets/food/{name}.png')
        
        ui_elements = self.create_ui_elements()
        for name, img in ui_elements.items():
            img.save(f'assets/ui/enhanced/{name}.png')
        
        with open('assets/asset_config.json', 'w', encoding='utf-8') as f:
            json.dump(self.asset_config, f, ensure_ascii=False, indent=2)
        
        print("✅ Enhanced assets generated successfully!")
        print("📁 Enhanced animations: assets/insects/enhanced/")
        print("🍯 Food items: assets/food/")
        print("🎮 UI elements: assets/ui/enhanced/")
        print("⚙️ Configuration: assets/asset_config.json")
    
    def create_animated_gif(self, frames, filename, duration=500):
        """Create animated GIF from frames"""
        if frames:
            frames[0].save(
                filename,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0
            )

if __name__ == "__main__":
    manager = AssetManager()
    manager.generate_all_assets()
