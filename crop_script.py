from PIL import Image
from os import listdir, path
from os import path
import sys


def crop(png_image_name, folderName):
    script_path = path.dirname(path.abspath(__file__))
    image_path = f'{script_path}\\{folderName}\\{png_image_name}'
    im = Image.open(image_path)
    im2 = im.crop(im.getbbox())
    im2.save(image_path)
    print(png_image_name, im2.size, f'Para uma altura de 64 pix, a largura ideal é:{(im2.size[1]*64)//im2.size[0]}')

try:
    folderName = sys.argv[1]
    for f in listdir(folderName):
        if f.endswith('.png'):
            crop(f, folderName)
except IndexError:
    print(f"Uso: python crop_script.py ../Pasta")
    exit()