from PIL import Image
import histogram_functions as hf

input_image = Image.open("input.png").convert("L")
input_image_pixels = input_image.load()

width,height = input_image.size

input_image_histogram = hf.build_histogram(input_image)
input_image_PDF = hf.build_PDF(input_image_histogram)
input_image_CDF = hf.build_CDF(input_image_PDF)
input_image_LUT = hf.build_lookup(input_image_CDF)

output_image = Image.new("L", (width,height))
output_image_pixels = output_image.load()

for y in range(height):
    for x in range(width):
        output_image_pixels[x,y] = input_image_LUT[input_image_pixels[x,y]]

output_image.save("EqualizedHisto.png") 