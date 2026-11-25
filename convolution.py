from PIL import Image

def convolution(input_image: Image.Image, kernel: list) -> Image.Image:
    kernel_height = len(kernel)
    kernel_width = len(kernel[0])

    input_image = input_image.convert("L")

    width, height = input_image.size
    input_pixels = input_image.load()

    output_image = Image.new("L", (width, height))
    output_pixels = output_image.load()

    padding_y = kernel_height // 2
    padding_x = kernel_width // 2

    for y in range(padding_y, height - padding_y):
        for x in range(padding_x, width - padding_x):

            accumulated_value = 0
            for kernel_y in range(kernel_height):
                for kernel_x in range(kernel_width):
                    input_x = x + kernel_x - padding_x
                    input_y = y + kernel_y - padding_y
                    input_pixel = input_pixels[input_x, input_y]

                    kernel_value = kernel[kernel_height - 1 - kernel_y][kernel_width - 1 - kernel_x]
                    accumulated_value += input_pixel * kernel_value

            output_pixels[x, y] = round(max(0, min(255, accumulated_value)))

    return output_image

