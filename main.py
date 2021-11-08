from collections import defaultdict
from PIL import Image
import sys


def has_alpha(pixel): 
    """
    Checks that a pixel is non-transparent
    """
    return pixel[3] != 0


def calculate_volume(image_path, rotation, board_thickness, board_length):
    image = Image.open(image_path).rotate(rotation, expand=True).convert('RGBA')
    all_pixels = image.getdata()
    partition = defaultdict(lambda: [sys.maxsize, -sys.maxsize+1])

    # Find min and max y coordinates of board at each point
    for x in range(image.width):
        for y in range(image.height):
            if has_alpha(all_pixels.getpixel((x, y))):
                partition[x][0] = min(partition[x][0], y)
                partition[x][1] = max(partition[x][1], y)

    # find integral of surface of the board
    x_coords = sorted(partition.keys())
    pixel_ratio = board_length / (x_coords[-1] - x_coords[0]) 
    xy_int = 0
    for x in x_coords:
        bot, top = partition[x]
        xy_int += (top-bot) * pixel_ratio**2

    # multiply volume by
    volume = xy_int * board_thickness
    return volume


def main():
    path = sys.argv[1]
    rotation, board_thickness, board_length = [float(i) for i in sys.argv[2:]]
    volume = calculate_volume(path, rotation, board_thickness, board_length)
    # convert inches^3 to liters
    liters = volume / 61.024
    print('Board volume is {:.2f} liters'.format(liters))


if __name__ == '__main__':
    """
    Call with 
    `python3 main.py [image_path] [rotation (degrees)] [board_thickness (inches)] [board_length(inches)]`
    """
    main()
