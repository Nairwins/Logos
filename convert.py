import os
from PIL import Image

# ----------------------------
# CONFIG
# ----------------------------
FOLDER = "re"
REFERENCE_IMAGE = "reference.png"  # set your reference image here

# ----------------------------
# Get target size from reference
# ----------------------------
def get_target_size(ref_path):
    with Image.open(ref_path) as img:
        return img.size  # (width, height)


# ----------------------------
# Convert + resize image → PNG
# ----------------------------
def process_image(path, target_size):
    try:
        with Image.open(path) as img:

            # Convert to RGBA (best for PNG quality + transparency)
            img = img.convert("RGBA")

            # Resize with high-quality filter
            img = img.resize(target_size, Image.LANCZOS)

            # New file path (force .png)
            new_path = os.path.splitext(path)[0] + ".png"

            # Save as PNG (lossless)
            img.save(new_path, "PNG", optimize=True)

        # Remove old file if different
        if path != new_path and os.path.exists(path):
            os.remove(path)

        print(f"✅ Converted: {os.path.basename(path)} → {os.path.basename(new_path)}")

    except Exception as e:
        print(f"❌ Failed: {path} ({e})")


# ----------------------------
# MAIN
# ----------------------------
def main():
    target_size = get_target_size(REFERENCE_IMAGE)
    print(f"🎯 Target size: {target_size}")

    for file in os.listdir(FOLDER):
        path = os.path.join(FOLDER, file)

        if not os.path.isfile(path):
            continue

        # skip reference image
        if file == REFERENCE_IMAGE:
            continue

        # only images
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            process_image(path, target_size)


# RUN
main()