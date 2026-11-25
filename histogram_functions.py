from PIL import Image

def build_histogram(image: Image.Image) -> list[int]:
    histogram = [0] * 256
    image_pixels = image.load()
    image_x, image_y = image.size

    for y in range(image_y):
        for x in range(image_x):
            histogram[image_pixels[x,y]] += 1

    return histogram

def build_PDF(histogram: list[int]) -> list[float]:
    total_pixels = sum(histogram)
    PDF = [0.0] * len(histogram)

    for intenisty,value in enumerate(histogram):
        PDF[intenisty] = value / total_pixels

    return PDF

def build_CDF(PDF: list[float]) -> list[float]:
    CDF = [0.0] * len(PDF)
    running_total = 0

    for intenisty,value in enumerate(PDF):
        running_total += value
        CDF[intenisty] = running_total

    return CDF

def build_lookup(CDF: list[float]) -> list[int]:
    LUT = [0] * len(CDF)

    for intenisty,value in enumerate(CDF):
        LUT[intenisty] = round(255 * value)

    return LUT
