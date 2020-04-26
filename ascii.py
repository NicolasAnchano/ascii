
from PIL import Image
from colorama import Fore, Style

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255

# Tuples containing color distribution
# 2-D array containing the matrix of pixels - a list of lists of tuples.
def create_pixel_matrix(img, height):
    img.thumbnail((height, 200))
    pixels = list(im.getdata())
    pixel_matrix = []
    for i in range(0, len(pixels), img.width):
        pixel_matrix.append(pixels[i:i+img.width])
    return pixel_matrix

# Getting the brightness of the pixel from the color of it
def rgb_to_brightness(pxl_mtrx, algo="average"):
    """
    algo defines the way we map RGB to brightness.
    """
    brightness_matrix = []
    for row in pxl_mtrx:
        brightness_row = []
        for p in row:
            if algo == "average":
                brightness = (p[0] + p[1] + p[2]) / 3
            elif algo == "max_min":
                brightness = (max(p) + min(p) / 2.0)
            elif algo == "luminosity":
                brightness = 0.21*p[0] + 0.72*p[1] + 0.07*p[2]
            else:
                raise Exception("Unrecognized algo name %s" % algo)
            brightness_row.append(brightness)
        brightness_matrix.append(brightness_row)
    return brightness_matrix

def normalize_brightness_matrix(brghtnss_mtrx):
    normalized_brightness_matrix = []
    max_pixel = max(map(max, brghtnss_mtrx))
    min_pixel = min(map(min, brghtnss_mtrx))
    for row in brghtnss_mtrx:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_brightness_matrix.append(rescaled_row)
    return normalized_brightness_matrix

def brightness_to_ascii(brghtnss_mtrx, ascii_chars):
    ascii_matrix = []
    for row in brghtnss_mtrx:
        ascii_row = []
        for p in row:
            # BRIGHTNESS TO ASCII FORMULA - pixel/max_pixel_value * total_ascii_characters
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)
    return ascii_matrix


def print_ascii_matrix(ascii_matrix, colour):
    # Fixing width when printing in the terminal and adding colour given by Fore module
    for row in ascii_matrix:
        line = [p+p+p for p in row]
        print(colour + "".join(line))
    print(Style.RESET_ALL)


filepath = "./first_input.jpg"

im = Image.open(filepath)
pixel_matrix = create_pixel_matrix(im, 1000)
brightness_matrix = rgb_to_brightness(pixel_matrix)
brightness_matrix = normalize_brightness_matrix(brightness_matrix)
ascii_matrix = brightness_to_ascii(brightness_matrix, ASCII_CHARS)
print_ascii_matrix(ascii_matrix, Fore.BLUE)
