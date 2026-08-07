import os
from PIL import Image, ImageDraw, ImageFont

# 1. Image Settings
WIDTH, HEIGHT = 1200, 675
BG_COLOR = (21, 13, 42)       # Dark Purple/Indigo (#150d2a)
SPECKLE_COLOR = (29, 58, 45)  # Green Glitch Speckles (#1d3a2d)
LIME = (198, 255, 0)          # Neon Lime Green (#c6ff00)
CYAN = (0, 229, 255)          # Neon Cyan (#00e5ff)
WHITE = (255, 255, 255)
MUTED = (160, 160, 160)

def create_promo_image():
    # Base Image
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # 2. Add Glitch Speckles to background
    import random
    random.seed(42) # Deterministic placement
    for _ in range(40):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        # Draw a blocky 8x8 pixel speckle
        draw.rectangle([x, y, x + 8, y + 8], fill=SPECKLE_COLOR)
        
    # Draw double border around canvas
    draw.rectangle([15, 15, WIDTH - 15, HEIGHT - 15], outline=CYAN, width=2)
    draw.rectangle([20, 20, WIDTH - 20, HEIGHT - 20], outline=LIME, width=1)
    
    # 3. Load and Draw NFT Cards on the Left Side
    assets_dir = "website/assets"
    nfts_to_show = ["nft_10.png", "nft_42.png"]
    nft_x_positions = [60, 370]
    nft_y = 160
    nft_size = 280
    
    for idx, nft_name in enumerate(nfts_to_show):
        nft_path = os.path.join(assets_dir, nft_name)
        if os.path.exists(nft_path):
            nft_img = Image.open(nft_path).convert("RGBA").resize((nft_size, nft_size), Image.Resampling.NEAREST)
            
            x_pos = nft_x_positions[idx]
            # Draw neon border behind card
            draw.rectangle([x_pos - 4, nft_y - 4, x_pos + nft_size + 4, nft_y + nft_size + 4], outline=CYAN, width=2)
            draw.rectangle([x_pos - 2, nft_y - 2, x_pos + nft_size + 2, nft_y + nft_size + 2], outline=LIME, width=2)
            
            # Paste NFT
            img.paste(nft_img, (x_pos, nft_y), nft_img)
            
            # Label banner below NFT card
            label_text = f"Onchain Mutineer #{nft_name.split('_')[1].split('.')[0]}"
            draw.rectangle([x_pos - 4, nft_y + nft_size + 10, x_pos + nft_size + 4, nft_y + nft_size + 34], fill=(12, 14, 18))
            draw.rectangle([x_pos - 4, nft_y + nft_size + 10, x_pos + nft_size + 4, nft_y + nft_size + 34], outline=CYAN, width=1)
            
            # Draw text inside label
            try:
                font_label = ImageFont.truetype("arial.ttf", 14)
            except:
                font_label = ImageFont.load_default()
            
            # Center text inside label
            w = draw.textlength(label_text, font=font_label)
            draw.text((x_pos + (nft_size - w)/2, nft_y + nft_size + 14), label_text, fill=LIME, font=font_label)
            
    # 4. Draw Typography on the Right Side (x=680 onwards)
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_detail_label = ImageFont.truetype("arial.ttf", 20)
        font_detail_val = ImageFont.truetype("arial.ttf", 22)
        font_tagline = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = font_subtitle = font_detail_label = font_detail_val = font_tagline = ImageFont.load_default()
        
    start_x = 680
    
    # Title aligned with card top (y=160)
    draw.text((start_x, 160), "ONCHAIN MUTINEERS", fill=LIME, font=font_title)
    
    # Subtitle
    draw.text((start_x, 215), "OFFICIAL MINT DETAILS", fill=CYAN, font=font_subtitle)
    
    # Divider line
    draw.line([start_x, 255, 1140, 255], fill=CYAN, width=2)
    
    # Mint details list
    details = [
        {"label": "DATE:", "val": "TODAY @ 6:00 PM UTC", "color": WHITE},
        {"label": "PRICE:", "val": "0.00055 ETH (100 FREE)", "color": LIME},
        {"label": "PLATFORM:", "val": "MINTING ON OPENSEA", "color": CYAN}
    ]
    
    current_y = 275
    for item in details:
        # Draw label in muted gray
        draw.text((start_x, current_y), item["label"], fill=MUTED, font=font_detail_label)
        # Draw value in custom color next to it (aligned in columns at x=840)
        draw.text((start_x + 160, current_y - 2), item["val"], fill=item["color"], font=font_detail_val)
        current_y += 50
        
    # Bottom Tagline aligned with the bottom of card labels (y=460)
    draw.text((start_x, 460), "Sail the digital seas. Plunder the vault.", fill=LIME, font=font_tagline)
    
    # Save Image
    output_path = "website/assets/twitter_promo.png"
    img.save(output_path)
    print(f"Generated Twitter promo image successfully at: {output_path}")

if __name__ == "__main__":
    create_promo_image()
