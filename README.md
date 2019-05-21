# deeppyer
[![PyPI](https://img.shields.io/pypi/v/deeppyer.svg)](https://pypi.org/project/deeppyer/)  
![banner image](https://raw.githubusercontent.com/Ovyerus/deeppyer/master/banner.jpg)

deeppyer is an image deepfryer written in Python using [Pillow](https://python-pillow.org/)
and [OpenCV](https://pypi.org/project/opencv-python/).

NOTE: This *requires* at least Python v3.6 in order to run.

## How to use
You can either use deeppyer as a module, or straight from the command line.

### Command line usage
```
$ python deeppyer.py -h

usage: deeppyer.py [-h] [-v] [-o OUTPUT] [-f] FILE

Deepfry an image.

positional arguments:
  FILE                  File to deepfry.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display program version.
  -o OUTPUT, --output OUTPUT
                        Filename to output to.
  -f, --flares          Try and detected faces for adding lens flares.
```

By default, flares will try to be added to the image, unless you're using the CLI script,
in which case it is off by default.

### Program usage
```py
from PIL import Image
import deeppyer, asyncio

async def main():
    img = Image.open('./foo.jpg')
    img = await deeppyer.deepfry(img)
    img.save('./bar.jpg')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## API Documentation
#### `async deepfry(img: Image, type=DeepfryTypes.RED, *, flares: bool = True)`
Deepfry a given image.

**Arguments**
 - *img* (PIL.Image) - Image to apply the deepfry effect on.
 - *[type]* (DeepfryTypes) - Colours to apply on the image.
 - *[flares] (bool) - Whether or not to try and detect faces for applying lens flares.

Returns:
  `PIL.Image` - Deepfried image.

## Why?
¯\\\_(ツ)_/¯ Why not

## Contributing
If you wish to contribute something to this, go ahead! Just please make sure to format it with flake8 + isort, and that the test(s) pass fine.

## Testing
Simply run `tests/test.py` and make sure that all the images output properly.
