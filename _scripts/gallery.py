import os
import json
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configure paths
image_dir = Path("images/lab")
output_file = image_dir / "gallery.json"

# Ensure the directory exists
image_dir.mkdir(parents=True, exist_ok=True)

files = []
supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

for file in image_dir.iterdir():
    if file.is_file() and file.suffix.lower() in supported_extensions:
        try:
            # Get file modification time
            mod_time = file.stat().st_mtime
            
            # Try to get image dimensions
            try:
                with Image.open(file) as img:
                    width, height = img.size
            except:
                width, height = None, None
            
            files.append({
                "name": file.name,
                "time": mod_time,
                "date": datetime.fromtimestamp(mod_time).isoformat(),
                "width": width,
                "height": height,
                "aspect_ratio": round(height / width, 3) if width and height else None
            })
        except Exception as e:
            print(f"Warning: Could not process {file.name}: {e}")

# Sort newest first
files.sort(key=lambda x: x["time"], reverse=True)

# Write to JSON file
with open(output_file, "w") as f:
    json.dump(files, f, indent=2)

# print(f"✅ Generated {output_file} with {len(files)} images")
# print(f"📁 Location: {output_file.absolute()}")