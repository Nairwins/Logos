from PIL import Image

def fix_logo(input_path, output_path, scale=0.9):
    img = Image.open(input_path).convert("RGBA")
    original_w, original_h = img.size  # keep original square

    # 1. Get bounding box (actual content)
    bbox = img.getbbox()
    if not bbox:
        print("Empty image")
        return

    cropped = img.crop(bbox)

    # 2. Resize content to be bigger
    target_size = int(min(original_w, original_h) * scale)

    # keep aspect ratio
    ratio = min(target_size / cropped.width, target_size / cropped.height)
    new_w = int(cropped.width * ratio)
    new_h = int(cropped.height * ratio)

    resized = cropped.resize((new_w, new_h), Image.LANCZOS)

    # 3. Create SAME SIZE square canvas
    new_img = Image.new("RGBA", (original_w, original_h), (0, 0, 0, 0))

    # 4. Center it
    x = (original_w - new_w) // 2
    y = (original_h - new_h) // 2

    new_img.paste(resized, (x, y), resized)

    new_img.save(output_path)
    print("✅ Done:", output_path)


# run it
fix_logo("bmw.png", "output.png", scale=0.92)