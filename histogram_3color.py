from PIL import Image
import histogram_functions as hf

input_image = Image.open("input.png").convert("RGB")
input_image_pixels = input_image.load()

width,height = input_image.size

(R,G,B) = input_image.split()

red_histogram = hf.build_histogram(R)
blue_histogram = hf.build_histogram(B)
green_histogram = hf.build_histogram(G)

red_PDF = hf.build_PDF(red_histogram)
blue_PDF = hf.build_PDF(blue_histogram)
green_PDF = hf.build_PDF(green_histogram)

red_CDF = hf.build_CDF(red_PDF)
blue_CDF = hf.build_CDF(blue_PDF)
green_CDF = hf.build_CDF(green_PDF)

red_LUT = hf.build_lookup(red_CDF)
blue_LUT = hf.build_lookup(blue_CDF)
green_LUT = hf.build_lookup(green_CDF)

output_image = Image.new("RGB", (width, height))
output_image_pixels = output_image.load()

for y in range(height):
    for x in range(width):
        red,green,blue = input_image_pixels[x,y]
        output_image_pixels[x,y] = (red_LUT[red], green_LUT[green], blue_LUT[blue])

output_image.save("equalized_3color.png")