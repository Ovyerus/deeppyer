import argparse
import asyncio
from collections import namedtuple
from enum import Enum
import math

from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy


# TODO: instead, take in tuples of colours
class DeepfryTypes(Enum):
    """
    Enum for the various possible effects added to the image.
    """
    RED = 1
    BLUE = 2


class Colours:
    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)
    BLUE = (36, 113, 229)
    WHITE = (255,) * 3


face_cascade = cv2.CascadeClassifier('./face_cascade.xml')
eye_cascade = cv2.CascadeClassifier('./eye_cascade.xml')
flare_img = Image.open('./flare.png')

FlarePosition = namedtuple('FlarePosition', ['x', 'y', 'size'])


async def deepfry(img: Image, type=DeepfryTypes.RED, *, flares: bool = True) -> Image:
    """
    Deepfry a given image.

    :param img: Image to manipulate.
    :param type: Colours to apply on the image.
    :param flares: Whether or not to try and detect faces for applying lens flares.
    :type img: PIL.Image
    :type type: DeepfryTypes
    :type flares: bool

    :returns: Deepfried image.
    :rtype: PIL.Image
    """
    if type not in DeepfryTypes:
        raise ValueError(f'Unknown deepfry type "{type}", expected a value from deeppyer.DeepfryTypes')

    img = img.copy().convert('RGB')
    flare_positions = []

    if flares:
        opencv_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(
            opencv_img,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            face_roi = opencv_img[y:y+h, x:x+w]  # Get region of interest (detected face)

            eyes = eye_cascade.detectMultiScale(face_roi)

            for (ex, ey, ew, eh) in eyes:
                eye_corner = (ex + ew / 2, ey + eh / 2)
                flare_size = eh if eh > ew else ew
                flare_size *= 4
                corners = [math.floor(x) for x in eye_corner]
                eye_corner = FlarePosition(*corners, flare_size)

                flare_positions.append(eye_corner)

    # Crush image to hell and back
    img = img.convert('RGB')
    width, height = img.width, img.height
    img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
    img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
    img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 4)

    # Generate red and yellow overlay for classic deepfry effect
    r = img.split()[0]
    r = ImageEnhance.Contrast(r).enhance(2.0)
    r = ImageEnhance.Brightness(r).enhance(1.5)

    if type == DeepfryTypes.RED:
        r = ImageOps.colorize(r, Colours.RED, Colours.YELLOW)
    elif type == DeepfryTypes.BLUE:
        r = ImageOps.colorize(r, Colours.BLUE, Colours.WHITE)

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, r, 0.75)
    img = ImageEnhance.Sharpness(img).enhance(100.0)

    # Apply flares on any detected eyes
    for flare in flare_positions:
        flare_transformed = flare_img.copy().resize((flare.size,) * 2, resample=Image.BILINEAR)
        img.paste(flare_transformed, (flare.x, flare.y), flare_transformed)

    return img

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deepfry an image.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='Display program version.')
    parser.add_argument('-o', '--output', help='Filename to output to.')
    parser.add_argument('-f', '--flares', help='Try and detected faces for adding lens flares.', action='store_true',
                        default=False)
    parser.add_argument('file', metavar='FILE', help='File to deepfry.')
    args = parser.parse_args()

    img = Image.open(args.file)
    out = args.output or './deepfried.jpg'

    loop = asyncio.get_event_loop()
    img = loop.run_until_complete(deepfry(img, flares=args.flares))

    img.save(out, 'jpeg')
