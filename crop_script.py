from PIL import Image
from os import listdir, path
from os import path
import sys


def crop(png_image_name, folderName):
    script_path = path.dirname(path.abspath(__file__))
    image_path = f'{script_path}/{folderName}/{png_image_name}'
    im = Image.open(image_path)
    #width, height = im.size
    #box_size = im.getbbox()
    #im2 = im.crop((width - box_size[2], box_size[1], box_size[2], box_size[3]))
    im2 = im.crop(im.getbbox())
    im2.save(image_path)

try:
    folderName = sys.argv[1]
    for f in listdir(folderName):
        if f.endswith('.png'):
            crop(f, folderName)
except IndexError:
    print(f"Uso: python crop_script.py ../Pasta")
    exit()