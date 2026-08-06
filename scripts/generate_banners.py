import os
from PIL import Image, ImageDraw, ImageFont

# Ensure the output directory exists
output_dir = 'C:/Users/CLASSIC/.gemini/antigravity-ide/brain/e6179fc3-4ead-4d26-a3b7-469b17ee5b11'
os.makedirs(output_dir, exist_ok=True)

# Load selected solid background NFTs
# 1: Acid Green + Robo Parrot
# 16: Neon Purple + No Companion
# 45: Steel Gray + No Companion
# 59: Deep Navy + No Companion
img_paths = {
    'parrot': 'scripts/output/images/1.png',
    'purple': 'scripts/output/images/16.png',
    'gray': 'scripts/output/images/45.png',
    'navy': 'scripts/output/images/59.png'
}

# Load and prepare images
nfts = {}
for key, path in img_paths.items():
    if os.path.exists(path):
        nfts[key] = Image.open(path).convert('RGBA')
    else:
        print(f'Warning: {path} not found.')
        nfts[key] = Image.new('RGBA', (200, 200), '#0b0e26')

# Setup fonts
try:
    font_title = ImageFont.truetype('arialbd.ttf', 44)
    font_title_small = ImageFont.truetype('arialbd.ttf', 38)
    font_subtitle = ImageFont.truetype('arialbd.ttf', 18)  # Bold and larger (size 18) for legibility
    font_ornament = ImageFont.truetype('arial.ttf', 20)
except:
    font_title = ImageFont.load_default()
    font_title_small = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_ornament = ImageFont.load_default()


# ==========================================
# DESIGN 1: DUAL SYMMETRY (2 ON LEFT, 2 ON RIGHT)
# ==========================================
canvas1 = Image.new('RGBA', (1500, 500), '#060814')
draw1 = ImageDraw.Draw(canvas1)

# Subtle grid
grid_color = (198, 255, 0, 10)
for x in range(0, 1500, 50):
    draw1.line([(x, 0), (x, 500)], fill=grid_color, width=1)
for y in range(0, 500, 50):
    draw1.line([(0, y), (1500, y)], fill=grid_color, width=1)

# NFTs list for Design 1
nft_list1 = [nfts['purple'], nfts['gray'], nfts['parrot'], nfts['navy']]
positions1 = [(40, 137), (260, 137), (1014, 137), (1234, 137)]
border_colors = ['#C6FF00', '#00E5FF', '#C6FF00', '#00E5FF']

for idx, (x, y) in enumerate(positions1):
    nft_res = nft_list1[idx].resize((210, 210), Image.Resampling.LANCZOS)
    card = Image.new('RGBA', (226, 226), '#0b0e26')
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, 225, 225], outline=border_colors[idx], width=2)
    card.paste(nft_res, (8, 8), nft_res)
    canvas1.paste(card, (x, y), card)

# Center Text (White subtitle for maximum legibility)
draw1.text((750, 180), 'ONCHAIN MUTINEERS', fill='#FFFFFF', font=font_title_small, anchor='mm')
draw1.text((750, 235), '*  *  *', fill='#C6FF00', font=font_ornament, anchor='mm')
draw1.text((750, 285), 'Sail the digital seas. Plunder the vault.', fill='#FFFFFF', font=font_subtitle, anchor='mm')
canvas1.save(os.path.join(output_dir, 'twitter_banner_design1.png'), 'PNG')


# ==========================================
# DESIGN 2: TOP-DOWN CARD DISPLAY
# ==========================================
canvas2 = Image.new('RGBA', (1500, 500), '#060814')
draw2 = ImageDraw.Draw(canvas2)

# Cyber grid
for x in range(0, 1500, 50):
    draw2.line([(x, 0), (x, 500)], fill=grid_color, width=1)
for y in range(0, 500, 50):
    draw2.line([(0, y), (1500, y)], fill=grid_color, width=1)

# Text at the top
draw2.text((750, 80), 'ONCHAIN MUTINEERS', fill='#FFFFFF', font=font_title, anchor='mm')
draw2.text((750, 135), 'Sail the digital seas. Plunder the vault.', fill='#FFFFFF', font=font_subtitle, anchor='mm')

# 4 NFTs side-by-side at the bottom
positions2 = [(220, 210), (510, 210), (800, 210), (1090, 210)]
nft_list2 = [nfts['purple'], nfts['gray'], nfts['navy'], nfts['parrot']]

for idx, (x, y) in enumerate(positions2):
    nft_res = nft_list2[idx].resize((180, 180), Image.Resampling.LANCZOS)
    card = Image.new('RGBA', (196, 196), '#0b0e26')
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, 195, 195], outline=border_colors[idx], width=2)
    card.paste(nft_res, (8, 8), nft_res)
    canvas2.paste(card, (x, y), card)

canvas2.save(os.path.join(output_dir, 'twitter_banner_design2.png'), 'PNG')


# ==========================================
# DESIGN 3: SPLIT GRID (LEFT GALLERY, RIGHT TEXT)
# ==========================================
canvas3 = Image.new('RGBA', (1500, 500), '#060814')
draw3 = ImageDraw.Draw(canvas3)

# Grid
for x in range(0, 1500, 50):
    draw3.line([(x, 0), (x, 500)], fill=grid_color, width=1)
for y in range(0, 500, 50):
    draw3.line([(0, y), (1500, y)], fill=grid_color, width=1)

# Overlapping card stack on the left
positions3 = [(60, 120), (220, 120), (380, 120), (540, 120)]
nft_list3 = [nfts['purple'], nfts['gray'], nfts['navy'], nfts['parrot']]

for idx, (x, y) in enumerate(positions3):
    nft_res = nft_list3[idx].resize((230, 230), Image.Resampling.LANCZOS)
    card = Image.new('RGBA', (246, 246), '#0b0e26')
    cdraw = ImageDraw.Draw(card)
    cdraw.rectangle([0, 0, 245, 245], outline=border_colors[idx], width=2)
    card.paste(nft_res, (8, 8), nft_res)
    canvas3.paste(card, (x, y), card)

# Right-aligned text
text_x = 1140
draw3.text((text_x, 190), 'ONCHAIN MUTINEERS', fill='#FFFFFF', font=font_title, anchor='mm')
draw3.text((text_x, 245), '*  *  *', fill='#C6FF00', font=font_ornament, anchor='mm')
draw3.text((text_x, 295), 'Sail the digital seas. Plunder the vault.', fill='#FFFFFF', font=font_subtitle, anchor='mm')

canvas3.save(os.path.join(output_dir, 'twitter_banner_design3.png'), 'PNG')

print("All 3 designs generated successfully!")
