import os
import random
from PIL import Image, ImageDraw

# Grid sizing for pixel art
GRID_SIZE = 32
CANVAS_SIZE = 1000

# Set paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAITS_DIR = os.path.join(SCRIPT_DIR, "traits")

# Layer order matching art_generator.py
LAYERS_ORDER = [
    "01_background",
    "02_body",
    "03_mouth",
    "04_eyes",
    "05_headwear",
    "06_pet",
    "07_overlay"
]

def make_canvas():
    """Create a transparent grid canvas."""
    return Image.new("RGBA", (GRID_SIZE, GRID_SIZE), (0, 0, 0, 0))

def scale_and_save(img, path):
    """Upscales pixel art using Nearest Neighbor for crisp edges and saves it."""
    scaled = img.resize((CANVAS_SIZE, CANVAS_SIZE), Image.NEAREST)
    scaled.save(path, "PNG")

def create_backgrounds():
    folder = os.path.join(TRAITS_DIR, "01_background")
    os.makedirs(folder, exist_ok=True)
    
    # Plain backgrounds as requested
    colors = {
        "Deep_Navy#100": (10, 15, 30, 255),
        "Cyber_Black#100": (15, 15, 18, 255),
        "Neon_Purple#100": (30, 10, 45, 255),
        "Acid_Green#100": (12, 28, 15, 255),
        "Synth_Red#100": (40, 10, 15, 255),
        "Steel_Gray#100": (35, 35, 40, 255),
        "Ocean_Muted#100": (10, 25, 35, 255)
    }
    
    for name, color in colors.items():
        img = Image.new("RGBA", (GRID_SIZE, GRID_SIZE), color)
        scale_and_save(img, os.path.join(folder, f"{name}.png"))

def create_bodies():
    folder = os.path.join(TRAITS_DIR, "02_body")
    os.makedirs(folder, exist_ok=True)
    
    skins = {
        "Chrome_Cyber#100": ((200, 200, 210, 255), (150, 150, 160, 255)),
        "Gold_Plate#5": ((255, 215, 0, 255), (200, 160, 0, 255)),
        "Robotic_Copper#100": ((184, 115, 51, 255), (130, 70, 30, 255)),
        "Hologram_Blue#60": ((0, 255, 255, 200), (0, 150, 200, 180)),
        "Plague_Green#100": ((80, 200, 120, 255), (40, 130, 70, 255))
    }
    
    for name, (primary, shadow) in skins.items():
        img = make_canvas()
        draw = ImageDraw.Draw(img)
        
        # Draw coat/torso (shoulders)
        draw.rectangle([6, 22, 25, 31], fill=(40, 40, 50, 255)) # Dark coat
        draw.rectangle([12, 22, 19, 31], fill=(20, 20, 25, 255)) # Shirt opening
        
        # Draw neck
        draw.rectangle([13, 19, 18, 22], fill=shadow)
        
        # Draw head/face shape
        draw.rectangle([10, 10, 21, 19], fill=primary)
        draw.rectangle([11, 19, 20, 19], fill=shadow) # Chin shadow
        
        # Ear details
        draw.point((9, 14), fill=shadow)
        draw.point((22, 14), fill=shadow)
        
        scale_and_save(img, os.path.join(folder, f"{name}.png"))

def create_mouths():
    folder = os.path.join(TRAITS_DIR, "03_mouth")
    os.makedirs(folder, exist_ok=True)
    
    # 1. Neutral mouth
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.line([(13, 17), (18, 17)], fill=(20, 20, 20, 255), width=1)
    scale_and_save(img, os.path.join(folder, "Neutral#100.png"))
    
    # 2. Smirk mouth
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.line([(13, 17), (17, 17)], fill=(20, 20, 20, 255), width=1)
    draw.point((18, 16), fill=(20, 20, 20, 255))
    scale_and_save(img, os.path.join(folder, "Smirk#100.png"))
    
    # 3. Cyan Cyber Grill
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([13, 16, 18, 17], fill=(0, 255, 255, 255))
    draw.line([(14, 16), (14, 17)], fill=(0, 100, 100, 255))
    draw.line([(16, 16), (16, 17)], fill=(0, 100, 100, 255))
    draw.line([(18, 16), (18, 17)], fill=(0, 100, 100, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Grill_Cyan#100.png"))

    # 4. Magenta Cyber Grill
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([13, 16, 18, 17], fill=(255, 0, 255, 255))
    draw.line([(14, 16), (14, 17)], fill=(100, 0, 100, 255))
    draw.line([(16, 16), (16, 17)], fill=(100, 0, 100, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Grill_Magenta#100.png"))

    # 5. Pirate Pipe mouth
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.line([(13, 17), (17, 17)], fill=(20, 20, 20, 255), width=1)
    # Pipe stem
    draw.line([(18, 17), (20, 18)], fill=(101, 67, 33, 255))
    # Pipe bowl
    draw.rectangle([21, 16, 22, 18], fill=(139, 69, 19, 255))
    # Glowing ember
    draw.point((21, 15), fill=(255, 100, 0, 255))
    scale_and_save(img, os.path.join(folder, "Pirate_Pipe#100.png"))

def create_eyes():
    folder = os.path.join(TRAITS_DIR, "04_eyes")
    os.makedirs(folder, exist_ok=True)
    
    # 1. Normal Robotic Eyes
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 13, 14, 14], fill=(255, 255, 255, 255))
    draw.point((13, 14), fill=(0, 255, 0, 255)) # Green pupil
    draw.rectangle([17, 13, 19, 14], fill=(255, 255, 255, 255))
    draw.point((18, 14), fill=(0, 255, 0, 255))
    scale_and_save(img, os.path.join(folder, "Robo_Eyes#100.png"))
    
    # 2. Glowing Cyan Eyepatch
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    # Right eye regular
    draw.rectangle([17, 13, 19, 14], fill=(255, 255, 255, 255))
    draw.point((18, 14), fill=(0, 255, 0, 255))
    # Left eye covered by neon patch
    draw.rectangle([11, 12, 14, 15], fill=(0, 255, 255, 255))
    draw.rectangle([12, 13, 13, 14], fill=(0, 150, 150, 255))
    # Eyepatch strap
    draw.line([(9, 11), (11, 12)], fill=(20, 20, 20, 255))
    draw.line([(14, 12), (21, 10)], fill=(20, 20, 20, 255))
    scale_and_save(img, os.path.join(folder, "Eyepatch_Cyan#100.png"))

    # 3. Glowing Magenta Eyepatch
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    # Right eye regular
    draw.rectangle([17, 13, 19, 14], fill=(255, 255, 255, 255))
    draw.point((18, 14), fill=(0, 255, 0, 255))
    # Left eye covered by neon patch
    draw.rectangle([11, 12, 14, 15], fill=(255, 0, 255, 255))
    draw.rectangle([12, 13, 13, 14], fill=(150, 0, 150, 255))
    # Eyepatch strap
    draw.line([(9, 11), (11, 12)], fill=(20, 20, 20, 255))
    draw.line([(14, 12), (21, 10)], fill=(20, 20, 20, 255))
    scale_and_save(img, os.path.join(folder, "Eyepatch_Magenta#100.png"))
    
    # 4. Holographic Visor
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([11, 12, 20, 15], fill=(255, 0, 255, 180)) # Translucent magenta visor
    draw.line([(12, 13), (19, 13)], fill=(0, 255, 255, 255)) # Cyan horizon line
    scale_and_save(img, os.path.join(folder, "VR_Visor#100.png"))

    # 5. Cyber Sunglasses
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([11, 12, 15, 14], fill=(10, 10, 15, 255))
    draw.rectangle([16, 12, 20, 14], fill=(10, 10, 15, 255))
    draw.line([(15, 12), (16, 12)], fill=(10, 10, 15, 255))
    # Cyber glow edge
    draw.line([(11, 15), (15, 15)], fill=(255, 255, 0, 255))
    draw.line([(16, 15), (20, 15)], fill=(255, 255, 0, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Shades#100.png"))

def create_headwear():
    folder = os.path.join(TRAITS_DIR, "05_headwear")
    os.makedirs(folder, exist_ok=True)
    
    # 1. Red Pirate Bandana
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 7, 21, 10], fill=(200, 30, 50, 255)) # Bandana cap
    draw.rectangle([9, 8, 9, 9], fill=(200, 30, 50, 255))
    draw.rectangle([22, 8, 22, 9], fill=(200, 30, 50, 255))
    # Knot on left ear
    draw.rectangle([8, 10, 9, 12], fill=(150, 15, 30, 255))
    scale_and_save(img, os.path.join(folder, "Pirate_Bandana_Red#100.png"))
    
    # 2. Cyan Cyber Bandana
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 7, 21, 10], fill=(0, 255, 255, 255))
    draw.rectangle([9, 8, 9, 9], fill=(0, 255, 255, 255))
    draw.rectangle([22, 8, 22, 9], fill=(0, 255, 255, 255))
    # Knot
    draw.rectangle([8, 10, 9, 12], fill=(0, 150, 150, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Bandana_Cyan#100.png"))

    # 3. Classic Pirate Tricorn Hat
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    # Brim (curved up sides)
    draw.rectangle([7, 7, 24, 8], fill=(45, 30, 20, 255))
    draw.point((7, 6), fill=(45, 30, 20, 255))
    draw.point((24, 6), fill=(45, 30, 20, 255))
    # Crown
    draw.rectangle([11, 4, 20, 6], fill=(45, 30, 20, 255))
    draw.rectangle([13, 3, 18, 3], fill=(45, 30, 20, 255))
    # Glowing Skull Emblem
    draw.rectangle([14, 5, 17, 6], fill=(0, 255, 255, 255))
    scale_and_save(img, os.path.join(folder, "Captain_Tricorn_Hat#5.png"))

    # 4. Cybernetic Mohawk
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([15, 3, 16, 9], fill=(255, 0, 255, 255)) # Glowing magenta mohawk
    draw.point((15, 2), fill=(255, 150, 255, 255))
    draw.point((16, 2), fill=(255, 150, 255, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Mohawk_Magenta#100.png"))

    # 5. Space Helmet
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    draw.rectangle([9, 6, 22, 11], fill=(120, 130, 150, 100)) # Glass dome (semi-trans)
    draw.line([(8, 11), (23, 11)], fill=(200, 200, 220, 255)) # Metal collar
    scale_and_save(img, os.path.join(folder, "Space_Dome#100.png"))
    
    # 6. None (Bare Head)
    img = make_canvas()
    scale_and_save(img, os.path.join(folder, "No_Headwear#100.png"))

def create_pets():
    folder = os.path.join(TRAITS_DIR, "06_pet")
    os.makedirs(folder, exist_ok=True)
    
    # 1. Cyber Shoulder Drone
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    # Drone body floating over right shoulder (left side of image)
    draw.rectangle([3, 16, 6, 18], fill=(100, 110, 120, 255))
    draw.point((4, 17), fill=(0, 255, 255, 255)) # Cyan sensor eye
    # Small rotors/antenna
    draw.line([(2, 15), (7, 15)], fill=(50, 50, 50, 255))
    scale_and_save(img, os.path.join(folder, "Cyber_Shoulder_Drone#100.png"))
    
    # 2. Cyber-Parrot (Green/Neon)
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    # Parrot body on shoulder
    draw.rectangle([3, 18, 5, 22], fill=(0, 200, 50, 255))
    # Wing
    draw.rectangle([2, 19, 2, 21], fill=(0, 150, 30, 255))
    # Beak
    draw.point((6, 19), fill=(255, 150, 0, 255))
    # Glowing eye
    draw.point((4, 18), fill=(255, 0, 255, 255))
    scale_and_save(img, os.path.join(folder, "Robo_Parrot#5.png"))
    
    # 3. None (No pet)
    img = make_canvas()
    scale_and_save(img, os.path.join(folder, "No_Companion#100.png"))

def create_overlays():
    folder = os.path.join(TRAITS_DIR, "07_overlay")
    os.makedirs(folder, exist_ok=True)
    
    # 1. Glitch Scanlines
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    for y in range(0, GRID_SIZE, 3):
        draw.line([(0, y), (GRID_SIZE, y)], fill=(0, 255, 255, 25)) # Very subtle cyan scanline
    scale_and_save(img, os.path.join(folder, "Glitch_Scanlines#100.png"))
    
    # 2. Binary Dust
    img = make_canvas()
    draw = ImageDraw.Draw(img)
    random.seed(42) # Deterministic noise
    for _ in range(30):
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        draw.point((x, y), fill=(0, 255, 0, 40)) # Light green digital dust
    scale_and_save(img, os.path.join(folder, "Binary_Dust#100.png"))
    
    # 3. None (Clean)
    img = make_canvas()
    scale_and_save(img, os.path.join(folder, "Clean_Overlay#100.png"))

def main():
    print("[*] Generating high-quality cyberpunk pixel art trait layers...")
    create_backgrounds()
    create_bodies()
    create_mouths()
    create_eyes()
    create_headwear()
    create_pets()
    create_overlays()
    print("[+] Trait generation complete! Folders populated in scripts/traits/")

if __name__ == "__main__":
    main()
