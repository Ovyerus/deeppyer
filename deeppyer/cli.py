import argparse
import asyncio

from PIL import Image

from . import deepfry


def main():
    parser = argparse.ArgumentParser(description='Deepfry an image.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0', help='Display program version.')
    parser.add_argument('-o', '--output', help='Filename to output to.')
    parser.add_argument('-f', '--flares', help='Try and detect faces for adding lens flares.', action='store_true',
                        default=False)
    parser.add_argument('file', metavar='FILE', help='File to deepfry.')
    args = parser.parse_args()

    img = Image.open(args.file)
    out = args.output or './deepfried.jpg'

    loop = asyncio.get_event_loop()
    img = loop.run_until_complete(deepfry(img, flares=args.flares))

    img.save(out, 'jpeg')
