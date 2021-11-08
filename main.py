from collections import defaultdict
from PIL import Image
import sys


def has_alpha(pixel): 
    """
    Checks that a pixel is non-transparent
    """
    return pixel[3] != 0


def calculate_volume(image_path, rotation, board_height, board_length):
    image = Image.open(image_path).rotate(rotation, expand=True).convert('RGBA')
    all_pixels = image.getdata()
    partition = defaultdict(lambda: [sys.maxsize, -sys.maxsize+1])

    # Find min and max height of board at each point
    for x in range(image.width):
        for y in range(image.height):
            if has_alpha(all_pixels.getpixel((x, y))):
                partition[x][0] = min(partition[x][0], y)
                partition[x][1] = max(partition[x][1], y)

    # find integral of surface of the board
    x_coords = sorted(partition.keys())
    pixel_ratio = board_length / (x_coords[-1] - x_coords[0]) 
    print(pixel_ratio)
    xy_int = 0
    for x in x_coords:
        bot, top = partition[x]
        xy_int += (top-bot) * pixel_ratio**2

    volume = xy_int * board_height
    return volume


def main():
#   path = '../res/board.png'
#   rotation = 270
#   board_height = 3
#   board_length = 66
    path, rotation, board_height, board_length = [int (i) for i in sys.argv[1:]]
    print(f'Board volume is {calculate_volume(path, rotation, board_height, board_length) / 61.024} liters')


if __name__ == '__main__':
    main()
