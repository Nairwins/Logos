from PIL import Image

def remove_white_bg(input_path, output_path, tolerance=240):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        r, g, b, a = item

        # detect near-white
        if r > tolerance and g > tolerance and b > tolerance:
            new_data.append((255, 255, 255, 0))  # transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

# usage
remove_white_bg("meta.png", "meta_no_bg.png")