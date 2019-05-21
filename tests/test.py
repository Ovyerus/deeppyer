import asyncio
import math

from PIL import Image

import deeppyer


async def main():
    print('[tests] Generating gradient image...')
    img = Image.new('RGB', (100, 100))

    for y in range(100):
        for x in range(100):
            distanceToCenter = math.sqrt((x - 100 / 2) ** 2 + (y - 100 / 2) ** 2)
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * 100 / 2)

            r = 0 * distanceToCenter + 255 * (1 - distanceToCenter)
            g = 0 * distanceToCenter + 255 * (1 - distanceToCenter)
            b = 0 * distanceToCenter + 255 * (1 - distanceToCenter)

            img.putpixel((x, y), (int(r), int(g), int(b)))

    img.save('./tests/gradient.jpg')

    print('[tests] Deepfrying gradient...')

    img2 = await deeppyer.deepfry(img)
    img2.save('./tests/gradient-fried.jpg')

    img2 = await deeppyer.deepfry(img, type=deeppyer.DeepfryTypes.BLUE)
    img2.save('./tests/gradient-fried-blue.jpg')

    print('[tests] Image successfully deepfried.'
          'Saved at `./test/gradient-fried.jpg`. and `./test/gradient-fried-blue.jpg`')

    print('[tests] Deepfrying `./test/test.jpg` with flares.')

    img = Image.open('./tests/human-test.jpg')

    img2 = await deeppyer.deepfry(img)
    img2.save('./tests/human-fried.jpg')

    img2 = await deeppyer.deepfry(img, type=deeppyer.DeepfryTypes.BLUE)
    img2.save('./tests/human-fried-blue.jpg')

    print('[tests] Human image successfully deepfried.'
          'Saved at `./test/human-fried.jpg` and `./test/human-fried-blue.jpg`.')

    print('[tests] All tests successfully completed.')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
