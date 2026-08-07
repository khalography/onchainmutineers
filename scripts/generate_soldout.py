import os
from PIL import Image, ImageDraw, ImageFont

def main():
    # 1. Create Canvas
    width, height = 1200, 675
    img = Image.new("RGBA", (width, height), (12, 14, 18, 255))
    draw = ImageDraw.Draw(img)
    
    # Theme colors
    CYAN = (0, 229, 255, 255)
    LIME = (198, 255, 0, 255)
    MAGENTA = (224, 64, 251, 255)
    WHITE = (255, 255, 255, 255)
    MUTED = (94, 100, 130, 255)
    
    # 2. Draw Digital Sea Wave background
    # Subtle matrix rain in background
    for i in range(12):
        for j in range(8):
            px = 50 + i * 100
            py = 40 + j * 80
            draw.rectangle([px, py, px + 2, py + 2], fill=(198, 255, 0, 30))
            
    # Draw double outer border
    draw.rectangle([10, 10, width - 10, height - 10], outline=CYAN, width=2)
    draw.rectangle([13, 13, width - 13, height - 13], outline=LIME, width=2)
    
    # 3. Draw Typography
    try:
        font_title = ImageFont.truetype("arial.ttf", 44)
        font_soldout = ImageFont.truetype("arial.ttf", 68)
        font_sub = ImageFont.truetype("arial.ttf", 22)
        font_footer = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = font_soldout = font_sub = font_footer = ImageFont.load_default()
        
    # Title (ONCHAIN MUTINEERS)
    title_text = "ONCHAIN MUTINEERS"
    w_title = draw.textlength(title_text, font=font_title)
    draw.text(((width - w_title)/2, 60), title_text, fill=LIME, font=font_title)
    
    # Sold out text (glowing)
    sold_text = "MINT SOLD OUT!"
    w_sold = draw.textlength(sold_text, font=font_soldout)
    draw.text(((width - w_sold)/2 + 2, 125 + 2), sold_text, fill=(0, 0, 0, 150), font=font_soldout) # shadow
    draw.text(((width - w_sold)/2, 125), sold_text, fill=MAGENTA, font=font_soldout)
    
    # 4. Load and Draw 3 NFT Cards side-by-side
    assets_dir = "website/assets"
    nfts = [
        {"name": "nft_10.png", "label": "Onchain Mutineer #10", "trait": "Gold Plate Skin"},
        {"name": "nft_42.png", "label": "Onchain Mutineer #42", "trait": "Cyber Mohawk"},
        {"name": "nft_200.png", "label": "Onchain Mutineer #200", "trait": "Robo Parrot"}
    ]
    
    card_size = 220
    card_y = 230
    x_positions = [230, 490, 750]
    
    for idx, item in enumerate(nfts):
        nft_path = os.path.join(assets_dir, item["name"])
        if os.path.exists(nft_path):
            nft_img = Image.open(nft_path).convert("RGBA").resize((card_size, card_size), Image.Resampling.NEAREST)
            x_pos = x_positions[idx]
            
            # Double card borders
            draw.rectangle([x_pos - 4, card_y - 4, x_pos + card_size + 4, card_y + card_size + 4], outline=CYAN, width=2)
            draw.rectangle([x_pos - 2, card_y - 2, x_pos + card_size + 2, card_y + card_size + 2], outline=LIME, width=2)
            
            # Paste NFT
            img.paste(nft_img, (x_pos, card_y), nft_img)
            
            # Draw label box below NFT card
            draw.rectangle([x_pos - 4, card_y + card_size + 10, x_pos + card_size + 4, card_y + card_size + 34], fill=(12, 14, 18))
            draw.rectangle([x_pos - 4, card_y + card_size + 10, x_pos + card_size + 4, card_y + card_size + 34], outline=CYAN, width=1)
            
            # Center label text inside banner
            try:
                font_label = ImageFont.truetype("arial.ttf", 13)
            except:
                font_label = ImageFont.load_default()
            w_label = draw.textlength(item["label"], font=font_label)
            draw.text((x_pos + (card_size - w_label)/2, card_y + card_size + 14), item["label"], fill=LIME, font=font_label)
            
    # 5. Tagline & Footer Links
    tagline = "1,111 unique pixel mutineers have successfully set sail."
    w_tag = draw.textlength(tagline, font=font_sub)
    draw.text(((width - w_tag)/2, 545), tagline, fill=WHITE, font=font_sub)
    
    footer_text = "Secondary trading is active. Verify the contract and join the crew on OpenSea."
    w_foot = draw.textlength(footer_text, font=font_footer)
    draw.text(((width - w_foot)/2, 595), footer_text, fill=CYAN, font=font_footer)
    
    # Save Image
    output_path = "website/assets/soldout_promo.png"
    img.save(output_path, "PNG")
    print(f"Generated Sold Out promo image successfully at: {output_path}")

if __name__ == "__main__":
    main()
