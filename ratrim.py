from PIL import Image
import os

def fix_logo(input_path, output_path, scale=0.9):
    img = Image.open(input_path).convert("RGBA")
    original_w, original_h = img.size

    bbox = img.getbbox()
    if not bbox:
        print("Empty image:", input_path)
        return

    cropped = img.crop(bbox)

    target_size = int(min(original_w, original_h) * scale)

    ratio = min(target_size / cropped.width, target_size / cropped.height)
    new_w = int(cropped.width * ratio)
    new_h = int(cropped.height * ratio)

    resized = cropped.resize((new_w, new_h), Image.LANCZOS)

    new_img = Image.new("RGBA", (original_w, original_h), (0, 0, 0, 0))

    x = (original_w - new_w) // 2
    y = (original_h - new_h) // 2

    new_img.paste(resized, (x, y), resized)

    new_img.save(output_path)
    print("✅ Done:", output_path)


# 🔁 Batch processing
input_folder = "re"
output_folder = "output"

# create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# supported formats
valid_ext = (".png", ".jpg", ".jpeg", ".webp")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_ext):
        input_path = os.path.join(input_folder, filename)

        # force output to PNG (since RGBA)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, name_without_ext + ".png")

        try:
            fix_logo(input_path, output_path, scale=0.92)
        except Exception as e:
            print("❌ Error with", filename, ":", e)