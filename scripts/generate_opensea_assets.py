import os
from PIL import Image

# 1. Colors Setup
BG_COLOR = (21, 13, 42)       # Flat Dark Purple/Indigo (#150d2a)
SPECKLE_COLOR = (29, 58, 45)  # Glitch Green Speckles (#1d3a2d)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (209, 35, 42)           # Flat Red Bandana (#d1232a)
DARK_GRAY = (43, 46, 51)      # Clothes/Steel Gray (#2b2e33)
LIGHT_GRAY = (122, 122, 122)  # Blade/Metal Gray (#7a7a7a)
YELLOW = (255, 204, 0)        # Skin/Gold Yellow (#ffcc00)
BROWN = (92, 58, 33)          # Chest wood brown (#5c3a21)

def create_pixel_canvas():
    img = Image.new("RGB", (24, 24), BG_COLOR)
    pixels = img.load()
    
    # Add glitch green speckles at identical positions matching the NFT style
    speckle_coords = [
        (5, 1), (12, 1), (20, 1), (9, 3), (13, 3), (18, 3), (2, 4), (10, 4), (17, 4),
        (21, 5), (0, 7), (8, 7), (17, 10), (1, 11), (20, 13), (8, 17), (14, 17), (21, 16)
    ]
    for x, y in speckle_coords:
        if 0 <= x < 24 and 0 <= y < 24:
            pixels[x, y] = SPECKLE_COLOR
            
    return img, pixels

def generate_logo():
    img, pixels = create_pixel_canvas()
    
    # Draw Crossed Swords behind skull
    # Sword 1: Top-Left to Bottom-Right
    sword_1 = [
        (3,3), (4,4), (5,5), (6,6), (7,7), (16,16), (17,17), (18,18), (19,19), (20,20)
    ]
    for x, y in sword_1:
        pixels[x, y] = LIGHT_GRAY
    # Handle 1
    pixels[21, 21] = YELLOW
    pixels[20, 21] = DARK_GRAY
    pixels[21, 20] = DARK_GRAY
    
    # Sword 2: Top-Right to Bottom-Left
    sword_2 = [
        (20,3), (19,4), (18,5), (17,6), (16,7), (7,16), (6,17), (5,18), (4,19), (3,20)
    ]
    for x, y in sword_2:
        pixels[x, y] = LIGHT_GRAY
    # Handle 2
    pixels[2, 21] = YELLOW
    pixels[3, 21] = DARK_GRAY
    pixels[2, 20] = DARK_GRAY

    # Draw Skull base shape (White)
    for y in range(8, 16):
        for x in range(8, 16):
            pixels[x, y] = WHITE
            
    # Jaw (White)
    for y in range(16, 19):
        for x in range(9, 15):
            pixels[x, y] = WHITE
            
    # Red Bandana (Red)
    # Bandana Tail
    pixels[5, 8] = RED
    pixels[6, 8] = RED
    pixels[6, 7] = RED
    # Bandana Main
    for y in range(6, 8):
        for x in range(7, 17):
            pixels[x, y] = RED
            
    # Eye holes (Black)
    pixels[9, 10] = BLACK
    pixels[10, 10] = BLACK
    pixels[13, 10] = BLACK
    pixels[14, 10] = BLACK
    
    # Nose hole (Black)
    pixels[11, 12] = BLACK
    pixels[12, 12] = BLACK
    
    # Teeth cuts (Black lines)
    pixels[10, 17] = BLACK
    pixels[12, 17] = BLACK
    pixels[13, 17] = BLACK
    
    # Upscale and Save
    img_resized = img.resize((1000, 1000), Image.Resampling.NEAREST)
    img_resized.save("website/assets/opensea_collection_logo.png")
    print("Generated collection logo successfully.")

def generate_prereveal():
    img, pixels = create_pixel_canvas()
    
    # Draw Chest base wood (Brown)
    for y in range(8, 18):
        for x in range(5, 19):
            pixels[x, y] = BROWN
            
    # Lid Partition (Black border)
    for x in range(5, 19):
        pixels[x, 11] = BLACK
        
    # Gold Lock plate
    for y in range(11, 13):
        for x in range(11, 13):
            pixels[x, y] = YELLOW
            
    # Keyhole in lock
    pixels[11, 12] = BLACK
    
    # Metal Brackets (Dark gray corners)
    # Top-Left
    pixels[5, 8] = DARK_GRAY
    pixels[6, 8] = DARK_GRAY
    pixels[5, 9] = DARK_GRAY
    # Top-Right
    pixels[18, 8] = DARK_GRAY
    pixels[17, 8] = DARK_GRAY
    pixels[18, 9] = DARK_GRAY
    # Bottom-Left
    pixels[5, 17] = DARK_GRAY
    pixels[6, 17] = DARK_GRAY
    pixels[5, 16] = DARK_GRAY
    # Bottom-Right
    pixels[18, 17] = DARK_GRAY
    pixels[17, 17] = DARK_GRAY
    pixels[18, 16] = DARK_GRAY
    
    # Chains wrapping the chest (Diagonal Light Gray lines)
    chain_1 = [
        (6,8), (7,9), (8,10), (9,11), (10,12), (13,13), (14,14), (15,15), (16,16), (17,17)
    ]
    for x, y in chain_1:
        pixels[x, y] = LIGHT_GRAY
        
    chain_2 = [
        (17,8), (16,9), (15,10), (14,11), (13,12), (10,13), (9,14), (8,15), (7,16), (6,17)
    ]
    for x, y in chain_2:
        pixels[x, y] = LIGHT_GRAY
        
    # Center Chain Ring overlay
    pixels[11, 13] = LIGHT_GRAY
    pixels[12, 13] = LIGHT_GRAY
    
    # Upscale and Save
    img_resized = img.resize((1000, 1000), Image.Resampling.NEAREST)
    img_resized.save("website/assets/prereveal_artwork.png")
    print("Generated prereveal chest artwork successfully.")

if __name__ == "__main__":
    generate_logo()
    generate_prereveal()
