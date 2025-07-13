from PIL import Image, ImageDraw
import os
import math

def create_beetle_frames():
    """Create 2-frame walking animation for beetle (カブトムシ) - brown, slow movement"""
    frames = []
    
    for frame in range(2):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([8, 12, 24, 20], fill=(139, 69, 19))
        
        draw.ellipse([10, 8, 14, 12], fill=(101, 67, 33))
        draw.ellipse([18, 8, 22, 12], fill=(101, 67, 33))
        
        draw.ellipse([11, 9, 13, 11], fill=(0, 0, 0))
        draw.ellipse([19, 9, 21, 11], fill=(0, 0, 0))
        
        leg_offset = 1 if frame == 1 else 0
        for i in range(3):
            y_offset = 14 + i * 2
            draw.line([(8, y_offset), (6 - leg_offset, y_offset + 2)], fill=(0, 0, 0), width=2)
            draw.line([(24, y_offset), (26 + leg_offset, y_offset + 2)], fill=(0, 0, 0), width=2)
        
        draw.polygon([(16, 8), (15, 5), (17, 5)], fill=(101, 67, 33))
        
        frames.append(img)
    
    return frames

def create_butterfly_frames():
    """Create 2-frame flying animation for butterfly (蝶々) - colorful, fluttery movement"""
    frames = []
    
    for frame in range(2):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.line([(16, 6), (16, 22)], fill=(0, 0, 0), width=2)
        
        draw.ellipse([14, 6, 18, 8], fill=(0, 0, 0))
        
        wing_offset = 2 if frame == 1 else 0
        
        draw.ellipse([10, 8 - wing_offset, 18, 12 - wing_offset], fill=(255, 105, 180))
        draw.ellipse([14, 8 - wing_offset, 22, 12 - wing_offset], fill=(255, 105, 180))
        
        draw.ellipse([12, 16 + wing_offset, 16, 20 + wing_offset], fill=(255, 182, 193))
        draw.ellipse([16, 16 + wing_offset, 20, 20 + wing_offset], fill=(255, 182, 193))
        
        draw.ellipse([12, 9 - wing_offset, 14, 11 - wing_offset], fill=(255, 255, 0))
        draw.ellipse([18, 9 - wing_offset, 20, 11 - wing_offset], fill=(255, 255, 0))
        
        frames.append(img)
    
    return frames

def create_ladybug_frames():
    """Create 2-frame walking animation for ladybug (てんとう虫) - red, quick movement"""
    frames = []
    
    for frame in range(2):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([10, 12, 22, 20], fill=(255, 0, 0))
        
        draw.ellipse([13, 14, 15, 16], fill=(0, 0, 0))
        draw.ellipse([17, 14, 19, 16], fill=(0, 0, 0))
        draw.ellipse([15, 17, 17, 19], fill=(0, 0, 0))
        
        draw.ellipse([12, 8, 20, 12], fill=(0, 0, 0))
        
        draw.ellipse([14, 9, 16, 11], fill=(255, 255, 255))
        draw.ellipse([16, 9, 18, 11], fill=(255, 255, 255))
        
        leg_offset = 2 if frame == 1 else 0
        for i in range(3):
            y_offset = 16 + i * 1
            draw.line([(10, y_offset), (8 - leg_offset, y_offset + 1)], fill=(0, 0, 0), width=1)
            draw.line([(22, y_offset), (24 + leg_offset, y_offset + 1)], fill=(0, 0, 0), width=1)
        
        frames.append(img)
    
    return frames

def create_caterpillar_frames():
    """Create 2-frame crawling animation for caterpillar (イモムシ) - green, slow crawling"""
    frames = []
    
    for frame in range(2):
        img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        segment_offset = 1 if frame == 1 else 0
        segments = [(8, 16), (12 + segment_offset, 16), (16, 16), (20 - segment_offset, 16), (24, 16)]
        
        for i, (x, y) in enumerate(segments):
            if i == 0:  # Head
                color = (34, 139, 34)
                size = 4
                draw.ellipse([x-size, y-2, x-size+2, y], fill=(0, 0, 0))
                draw.ellipse([x-size, y, x-size+2, y+2], fill=(0, 0, 0))
            else:  # Body segments
                color = (50, 205, 50)
                size = 3
            
            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
        
        for i, (x, y) in enumerate(segments[1:], 1):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(34, 139, 34))
        
        frames.append(img)
    
    return frames

def create_animated_gif(frames, filename, duration=500):
    """Create animated GIF from frames"""
    if frames:
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )

def create_static_sprites():
    """Create static PNG versions for fallback"""
    beetle_frames = create_beetle_frames()
    butterfly_frames = create_butterfly_frames()
    ladybug_frames = create_ladybug_frames()
    caterpillar_frames = create_caterpillar_frames()
    
    beetle_frames[0].save('assets/insects/beetle_static.png')
    butterfly_frames[0].save('assets/insects/butterfly_static.png')
    ladybug_frames[0].save('assets/insects/ladybug_static.png')
    caterpillar_frames[0].save('assets/insects/caterpillar_static.png')

def create_additional_species():
    """Create assets for additional species mentioned in unlock system"""
    
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.line([(16, 8), (16, 24)], fill=(0, 100, 0), width=2)
    
    draw.ellipse([8, 10, 16, 14], fill=(200, 200, 255, 150))
    draw.ellipse([16, 10, 24, 14], fill=(200, 200, 255, 150))
    draw.ellipse([8, 16, 16, 20], fill=(200, 200, 255, 150))
    draw.ellipse([16, 16, 24, 20], fill=(200, 200, 255, 150))
    
    draw.ellipse([14, 6, 18, 10], fill=(0, 100, 0))
    
    draw.ellipse([13, 7, 15, 9], fill=(255, 0, 0))
    draw.ellipse([17, 7, 19, 9], fill=(255, 0, 0))
    
    img.save('assets/insects/dragonfly.png')
    
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([8, 14, 12, 18], fill=(0, 0, 0))  # Abdomen
    draw.ellipse([12, 12, 16, 16], fill=(0, 0, 0))  # Thorax
    draw.ellipse([16, 10, 20, 14], fill=(0, 0, 0))  # Head
    
    for i in range(3):
        y_offset = 14 + i * 1
        draw.line([(12, y_offset), (10, y_offset + 2)], fill=(0, 0, 0), width=1)
        draw.line([(14, y_offset), (16, y_offset + 2)], fill=(0, 0, 0), width=1)
    
    draw.line([(17, 10), (15, 8)], fill=(0, 0, 0), width=1)
    draw.line([(19, 10), (21, 8)], fill=(0, 0, 0), width=1)
    
    img.save('assets/insects/ant.png')

os.makedirs('assets/insects/animated', exist_ok=True)

print("Creating animated insect sprites...")

beetle_frames = create_beetle_frames()
create_animated_gif(beetle_frames, 'assets/insects/animated/beetle_walk.gif', duration=600)

butterfly_frames = create_butterfly_frames()
create_animated_gif(butterfly_frames, 'assets/insects/animated/butterfly_fly.gif', duration=400)

ladybug_frames = create_ladybug_frames()
create_animated_gif(ladybug_frames, 'assets/insects/animated/ladybug_walk.gif', duration=300)

caterpillar_frames = create_caterpillar_frames()
create_animated_gif(caterpillar_frames, 'assets/insects/animated/caterpillar_crawl.gif', duration=800)

create_static_sprites()

create_additional_species()

print("✅ All animated insect assets created successfully!")
print("📁 Animated GIFs saved in: assets/insects/animated/")
print("🐛 Created animations for:")
print("  - beetle_walk.gif (カブトムシ - brown, slow)")
print("  - butterfly_fly.gif (蝶々 - colorful, fluttery)")
print("  - ladybug_walk.gif (てんとう虫 - red, quick)")
print("  - caterpillar_crawl.gif (イモムシ - green, slow crawling)")
print("📄 Static PNG fallbacks also created")
print("🆕 Additional species: dragonfly.png, ant.png")
