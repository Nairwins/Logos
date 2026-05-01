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

            img = img.convert("RGBA")

            target_w, target_h = target_size

            # 1. Resize while keeping aspect ratio
            img.thumbnail((target_w, target_h), Image.LANCZOS)

            # 2. Create transparent canvas (same as reference)
            new_img = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

            # 3. Center the image
            x = (target_w - img.width) // 2
            y = (target_h - img.height) // 2

            new_img.paste(img, (x, y), img)

            # Save as PNG
            new_path = os.path.splitext(path)[0] + ".png"
            new_img.save(new_path, "PNG", optimize=True)

        if path != new_path and os.path.exists(path):
            os.remove(path)

        print(f"✅ Fixed: {os.path.basename(path)}")

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