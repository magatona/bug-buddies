from PIL import Image, ImageDraw
import os
import math

def create_grass_sprite():
    img = Image.new('RGBA', (16, 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon([(2, 8), (4, 2), (6, 8)], fill=(34, 139, 34))
    draw.polygon([(6, 8), (8, 1), (10, 8)], fill=(50, 205, 50))
    draw.polygon([(10, 8), (12, 3), (14, 8)], fill=(34, 139, 34))
    return img

def create_flower_sprite():
    img = Image.new('RGBA', (12, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    for angle in [0, 72, 144, 216, 288]:
        x = 6 + 3 * math.cos(math.radians(angle))
        y = 6 + 3 * math.sin(math.radians(angle))
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 192, 203))
    
    draw.ellipse([4, 4, 8, 8], fill=(255, 255, 0))
    return img

def create_beetle_sprite():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([8, 12, 24, 20], fill=(139, 69, 19))
    draw.ellipse([10, 8, 14, 12], fill=(101, 67, 33))
    draw.ellipse([18, 8, 22, 12], fill=(101, 67, 33))
    draw.ellipse([11, 9, 13, 11], fill=(0, 0, 0))
    draw.ellipse([19, 9, 21, 11], fill=(0, 0, 0))
    
    for i in range(3):
        y_offset = 14 + i * 2
        draw.line([(8, y_offset), (6, y_offset + 2)], fill=(0, 0, 0), width=1)
        draw.line([(24, y_offset), (26, y_offset + 2)], fill=(0, 0, 0), width=1)
    
    return img

def create_butterfly_sprite():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([10, 8, 18, 12], fill=(255, 105, 180))
    draw.ellipse([14, 8, 22, 12], fill=(255, 105, 180))
    
    draw.ellipse([12, 16, 16, 20], fill=(255, 182, 193))
    draw.ellipse([16, 16, 20, 20], fill=(255, 182, 193))
    
    draw.line([(16, 6), (16, 22)], fill=(0, 0, 0), width=2)
    
    draw.ellipse([14, 6, 18, 8], fill=(0, 0, 0))
    
    return img

def create_ladybug_sprite():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([10, 12, 22, 20], fill=(255, 0, 0))
    
    draw.ellipse([13, 14, 15, 16], fill=(0, 0, 0))
    draw.ellipse([17, 14, 19, 16], fill=(0, 0, 0))
    draw.ellipse([16, 17, 18, 19], fill=(0, 0, 0))
    
    draw.ellipse([12, 8, 20, 12], fill=(0, 0, 0))
    
    draw.ellipse([14, 9, 16, 11], fill=(255, 255, 255))
    draw.ellipse([16, 9, 18, 11], fill=(255, 255, 255))
    
    return img

def create_caterpillar_sprite():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    segments = [(8, 16), (12, 16), (16, 16), (20, 16), (24, 16)]
    
    for i, (x, y) in enumerate(segments):
        color = (34, 139, 34) if i == 0 else (50, 205, 50)
        size = 4 if i == 0 else 3
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    draw.ellipse([6, 14, 8, 16], fill=(0, 0, 0))
    draw.ellipse([6, 16, 8, 18], fill=(0, 0, 0))
    
    return img

def create_ui_elements():
    settings_icon = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(settings_icon)
    
    draw.ellipse([6, 6, 10, 10], outline=(128, 128, 128), width=1)
    draw.ellipse([7, 7, 9, 9], fill=(128, 128, 128))
    
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        x1 = 8 + 4 * math.cos(math.radians(angle))
        y1 = 8 + 4 * math.sin(math.radians(angle))
        x2 = 8 + 6 * math.cos(math.radians(angle))
        y2 = 8 + 6 * math.sin(math.radians(angle))
        draw.line([(x1, y1), (x2, y2)], fill=(128, 128, 128), width=1)
    
    return settings_icon

os.makedirs('assets/environment', exist_ok=True)
os.makedirs('assets/insects', exist_ok=True)
os.makedirs('assets/ui', exist_ok=True)

create_grass_sprite().save('assets/environment/grass.png')
create_flower_sprite().save('assets/environment/flower.png')

create_beetle_sprite().save('assets/insects/beetle.png')
create_butterfly_sprite().save('assets/insects/butterfly.png')
create_ladybug_sprite().save('assets/insects/ladybug.png')
create_caterpillar_sprite().save('assets/insects/caterpillar.png')

create_ui_elements().save('assets/ui/settings.png')

print('All art assets created successfully!')
print('Environment assets: grass.png, flower.png')
print('Insect sprites: beetle.png, butterfly.png, ladybug.png, caterpillar.png')
print('UI elements: settings.png')
