from PIL import Image


def median_stacking(k: int, input_image: Image.Image):
    images = [input_image.convert("RGB")]

    for i in range(1, k):
        file_name = f"frame_{i:03d}.png"
        images.append(Image.open(file_name).convert("RGB"))

    width, height = images[0].size

    result_image = Image.new("RGB", (width,height))
    result_pixels = result_image.load()

    for y in range(height):
        for x in range(width):

            r_values = []
            g_values = []
            b_values = []

            for img in images:
                r,g,b = img.getpixel((x,y))
                r_values.append(r)
                g_values.append(g)
                b_values.append(b)

            r_values.sort()
            g_values.sort()
            b_values.sort()

            middle_index = k//2
            median_r = r_values[middle_index]
            median_b = b_values[middle_index]
            median_g = g_values[middle_index]

            result_pixels[x,y] = (median_r, median_g,median_b)


    result_image.save(f"output_k_{k}_python.jpg")
