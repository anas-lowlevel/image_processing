from math import atan2, degrees, hypot
from PIL import Image
from convolution import convolution


def canny_edge_detection(
    input_image: Image.Image,
    low_threshold: float = 30,
    high_threshold: float = 80,
) -> Image.Image:
    
    gaussian_kernel = [
        [1 / 16, 2 / 16, 1 / 16],
        [2 / 16, 4 / 16, 2 / 16],
        [1 / 16, 2 / 16, 1 / 16],
    ]
    smoothed_image = convolution(input_image, gaussian_kernel)
    smoothed_pixels = smoothed_image.load()
    width, height = smoothed_image.size

    sobel_x = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ]
    sobel_y = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ]
    magnitudes = [[0.0] * width for _ in range(height)]
    directions = [[0.0] * width for _ in range(height)]

    
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            gradient_x = 0
            gradient_y = 0

            for kernel_y in range(3):
                for kernel_x in range(3):
                    pixel = smoothed_pixels[x + kernel_x - 1, y + kernel_y - 1]
                    gradient_x += pixel * sobel_x[kernel_y][kernel_x]
                    gradient_y += pixel * sobel_y[kernel_y][kernel_x]

            magnitudes[y][x] = hypot(gradient_x, gradient_y)
            directions[y][x] = degrees(atan2(gradient_y, gradient_x)) % 180

    result_image = Image.new("L", (width, height))
    result_pixels = result_image.load()
    weak_edges = set()
    strong_edges = []

    
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            direction = directions[y][x]
            if direction < 22.5 or direction >= 157.5:
                offset_x, offset_y = 1, 0
            elif direction < 67.5:
                offset_x, offset_y = 1, 1
            elif direction < 112.5:
                offset_x, offset_y = 0, 1
            else:
                offset_x, offset_y = -1, 1

            magnitude = magnitudes[y][x]
            before = magnitudes[y - offset_y][x - offset_x]
            after = magnitudes[y + offset_y][x + offset_x]

            if magnitude <= before or magnitude < after:
                continue

            if magnitude >= high_threshold:
                result_pixels[x, y] = 255
                strong_edges.append((x, y))
            elif magnitude >= low_threshold:
                weak_edges.add((x, y))

    
    while strong_edges:
        x, y = strong_edges.pop()
        for neighbor_y in range(y - 1, y + 2):
            for neighbor_x in range(x - 1, x + 2):
                neighbor = (neighbor_x, neighbor_y)
                if neighbor in weak_edges:
                    weak_edges.remove(neighbor)
                    result_pixels[neighbor] = 255
                    strong_edges.append(neighbor)

    return result_image


if __name__ == "__main__":
    input_file = "input.png"
    output_file = "canny_edges.png"
    low_threshold = 30
    high_threshold = 80

    with Image.open(input_file) as input_image:
        result_image = canny_edge_detection(input_image, low_threshold, high_threshold)

    result_image.save(output_file)
