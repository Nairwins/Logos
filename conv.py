import os
import subprocess

os.makedirs("svgs", exist_ok=True)

ICON_DIR = "icons"
SVG_DIR = "svgs"

def convert_png_to_svg(png_path, svg_path):
    try:
        # Step 1: convert PNG → BMP (required for potrace)
        bmp_path = png_path.replace(".png", ".bmp")
        subprocess.run(["convert", png_path, bmp_path], check=True)

        # Step 2: BMP → SVG
        subprocess.run(["potrace", bmp_path, "-s", "-o", svg_path], check=True)

        # Cleanup BMP
        os.remove(bmp_path)

        return True
    except Exception as e:
        print("❌ Error:", e)
        return False


def process_icons():
    files = [f for f in os.listdir(ICON_DIR) if f.endswith(".png")]

    for i, file in enumerate(files, 1):
        png_path = os.path.join(ICON_DIR, file)
        svg_name = file.replace(".png", ".svg")
        svg_path = os.path.join(SVG_DIR, svg_name)

        print(f"[{i}] 🔄 {file}")

        success = convert_png_to_svg(png_path, svg_path)

        if success:
            print("✅ SVG created")
        else:
            print("❌ Failed")


process_icons()