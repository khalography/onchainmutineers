import os
import json
import random
from PIL import Image

# ==========================================
# CONFIGURATION
# ==========================================
TOTAL_SUPPLY = 1111  # Number of unique NFTs to generate
PROJECT_NAME = "Onchain Mutineer"
DESCRIPTION = """1,111 pixel mutineers sailing the digital seas of the Robinhood chain.

The old financial world lies in ruins. Out here on the decentralized waves, only the crew matters. Onchain Mutineers is a gamified, community-driven NFT collection featuring a weekly reward vault, dynamic storm sell taxes, and a strict holding streak mechanic.

Stake your Mutineer, build your holding multiplier, and join the Saturday Crew Votes to decide our next heist. Will we bury the loot to burn the supply, or plunder the vault to reward the loyal?

The choice is yours. Welcome to the crew. 🏴☠️"""
BASE_IMAGE_URI = "ipfs://QmYourCollectionHashHere/"  # Replace with your IPFS hash after uploading

# The order of these directories determines the layering order (bottom to top)
LAYERS_ORDER = [
    "01_background",
    "02_body",
    "03_mouth",
    "04_eyes",
    "05_headwear",
    "06_pet",
    "07_overlay"
]

# Set paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRAITS_DIR = os.path.join(SCRIPT_DIR, "traits")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
IMAGES_OUT = os.path.join(OUTPUT_DIR, "images")
METADATA_OUT = os.path.join(OUTPUT_DIR, "metadata")

def setup_directories():
    """Create directory structure if it doesn't exist."""
    for layer in LAYERS_ORDER:
        os.makedirs(os.path.join(TRAITS_DIR, layer), exist_ok=True)
    os.makedirs(IMAGES_OUT, exist_ok=True)
    os.makedirs(METADATA_OUT, exist_ok=True)
    
    # Check if folders are empty, create placeholders if so
    is_empty = all(len(os.listdir(os.path.join(TRAITS_DIR, layer))) == 0 for layer in LAYERS_ORDER)
    if is_empty:
        print("\n[!] Created 'traits/' folders. Please populate each folder with transparent .png assets.")
        print("    Tip: Use filename format 'TraitName#Weight.png' (e.g. 'GoldEyePatch#5.png') to set rarity weights.")
        print("    If no '#Weight' is in the filename, it defaults to a weight of 100.\n")
        # Create a dummy trait in each folder just so the script runs as a test if needed
        for i, layer in enumerate(LAYERS_ORDER):
            dummy_path = os.path.join(TRAITS_DIR, layer, f"placeholder_trait_for_{layer}#100.png")
            img = Image.new("RGBA", (1000, 1000), color=(
                random.randint(0, 255) if i == 0 else 0,
                random.randint(0, 255) if i == 0 else 0,
                random.randint(0, 255) if i == 0 else 0,
                255 if i == 0 else 50
            ))
            img.save(dummy_path)
        print("[*] Generated colorful placeholder assets. You can run the script to see a test run.")

def parse_traits():
    """Scans traits directory and returns dictionaries of assets and their weights."""
    traits_data = {}
    for layer in LAYERS_ORDER:
        layer_path = os.path.join(TRAITS_DIR, layer)
        files = [f for f in os.listdir(layer_path) if f.endswith('.png')]
        
        assets = []
        weights = []
        
        for file in files:
            # Parse weight from filename (e.g. "GoldEyePatch#5.png" -> name="GoldEyePatch", weight=5)
            name_part = file.rsplit('.', 1)[0]
            if "#" in name_part:
                trait_name, weight_str = name_part.split("#", 1)
                try:
                    weight = float(weight_str)
                except ValueError:
                    weight = 100.0
            else:
                trait_name = name_part
                weight = 100.0
                
            assets.append({
                "filename": file,
                "trait_name": trait_name.replace("_", " ").title(),
                "path": os.path.join(layer_path, file)
            })
            weights.append(weight)
            
        traits_data[layer] = {
            "assets": assets,
            "weights": weights
        }
    return traits_data

def generate_unique_combinations(traits_data, count):
    """Generates unique configurations of traits up to 'count'."""
    combinations = []
    seen = set()
    
    # Calculate max possible combinations to prevent infinite loops
    max_combos = 1
    for layer in LAYERS_ORDER:
        max_combos *= len(traits_data[layer]["assets"])
        
    actual_count = min(count, max_combos)
    if actual_count < count:
        print(f"\n[Warning] Only {max_combos} unique combinations are possible with current assets.")
        print(f"Generating {max_combos} NFTs instead of requested {count}.\n")
        
    attempts = 0
    while len(combinations) < actual_count and attempts < count * 10:
        combo = {}
        combo_sig = []
        
        for layer in LAYERS_ORDER:
            layer_info = traits_data[layer]
            if not layer_info["assets"]:
                raise ValueError(f"No traits found in layer: {layer}")
                
            # Weighted random selection
            selected = random.choices(layer_info["assets"], weights=layer_info["weights"], k=1)[0]
            combo[layer] = selected
            combo_sig.append(selected["filename"])
            
        sig = ",".join(combo_sig)
        if sig not in seen:
            seen.add(sig)
            combinations.append(combo)
            
        attempts += 1
        
    return combinations

def build_nft_images_and_metadata(combinations):
    """Processes combination lists, composites images, and saves metadata."""
    print(f"\n[*] Generating {len(combinations)} NFTs...")
    
    # Track statistics for rarity report
    rarity_stats = {layer: {} for layer in LAYERS_ORDER}
    
    for idx, combo in enumerate(combinations):
        token_id = idx + 1
        
        # 1. Image Compositing
        base_img = None
        attributes = []
        
        for layer in LAYERS_ORDER:
            trait = combo[layer]
            trait_name = trait["trait_name"]
            
            # Record rarity stats
            rarity_stats[layer][trait_name] = rarity_stats[layer].get(trait_name, 0) + 1
            
            # Add to ERC-721 attributes array
            # Format layer folder name for display type (e.g. "01_background" -> "Background")
            display_layer_name = layer.split("_", 1)[1].replace("_", " ").title()
            attributes.append({
                "trait_type": display_layer_name,
                "value": trait_name
            })
            
            # Composite images
            layer_img = Image.open(trait["path"]).convert("RGBA")
            if base_img is None:
                base_img = layer_img
            else:
                assert base_img is not None
                base_img = Image.alpha_composite(base_img, layer_img)
                
        # Save image
        img_filename = f"{token_id}.png"
        if base_img is not None:
            base_img.save(os.path.join(IMAGES_OUT, img_filename), "PNG")
        else:
            raise ValueError("No layers were found to composite the NFT image.")
        
        # 2. Metadata Generation
        metadata = {
            "name": f"{PROJECT_NAME} #{token_id}",
            "description": DESCRIPTION,
            "image": f"{BASE_IMAGE_URI}{token_id}.png",
            "edition": token_id,
            "attributes": attributes
        }
        
        # Save metadata JSON
        metadata_filename = f"{token_id}.json"
        with open(os.path.join(METADATA_OUT, metadata_filename), "w") as f:
            json.dump(metadata, f, indent=4)
            
        if token_id % 100 == 0 or token_id == len(combinations):
            print(f" -> Generated {token_id}/{len(combinations)}")
            
    return rarity_stats

def print_rarity_report(rarity_stats, total):
    """Outputs a rarity distribution report to a text file and terminal."""
    report_lines = [
        "==========================================",
        f"RARITY REPORT - {PROJECT_NAME}",
        f"Total Collection Size: {total}",
        "=========================================="
    ]
    
    for layer in LAYERS_ORDER:
        display_layer_name = layer.split("_", 1)[1].replace("_", " ").title()
        report_lines.append(f"\nLayer: {display_layer_name}")
        report_lines.append("-" * len(display_layer_name))
        
        # Sort traits by occurrence (ascending rarity)
        sorted_traits = sorted(rarity_stats[layer].items(), key=lambda x: x[1])
        for trait_name, count in sorted_traits:
            percentage = (count / total) * 100
            report_lines.append(f"  - {trait_name}: {count} ({percentage:.2f}%)")
            
    # Write to file
    report_path = os.path.join(OUTPUT_DIR, "rarity_report.txt")
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"\n[+] Generation completed! Files saved in: {OUTPUT_DIR}")
    print(f"[+] Rarity distribution report saved to: {report_path}\n")

def generate_opensea_csv(combinations):
    """Generates the OpenSea Drop metadata-file.csv."""
    import csv
    csv_path = os.path.join(OUTPUT_DIR, "metadata-file.csv")
    print(f"\n[*] Compiling OpenSea Drop CSV metadata file at: {csv_path}...")
    
    # Headers matching OpenSea Drop specs
    headers = ["tokenID", "name", "file_name", "external_url"]
    for layer in LAYERS_ORDER:
        display_layer_name = layer.split("_", 1)[1].replace("_", " ").title()
        headers.append(f"attributes[{display_layer_name}]")
        
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for idx, combo in enumerate(combinations):
            token_id = idx + 1
            row = [
                token_id,
                f"{PROJECT_NAME} #{token_id}",
                f"{token_id}.png",
                "https://onchainmutineers.site"
            ]
            for layer in LAYERS_ORDER:
                row.append(combo[layer]["trait_name"])
            writer.writerow(row)
            
    print(f"[+] OpenSea Drop CSV metadata file successfully compiled!")

def main():
    setup_directories()
    traits_data = parse_traits()
    
    try:
        combinations = generate_unique_combinations(traits_data, TOTAL_SUPPLY)
        stats = build_nft_images_and_metadata(combinations)
        print_rarity_report(stats, len(combinations))
        generate_opensea_csv(combinations)
    except Exception as e:
        print(f"\n[Error] Failed to generate collection: {e}")
        print("Please check that all trait PNGs are matching sizes and RGBA transparent format.")

if __name__ == "__main__":
    main()
