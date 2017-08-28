from PIL import Image
import asyncio, math, json, deeppyer

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
    img = await deeppyer.deepfry(img)
    img.save('./tests/gradient-fried.jpg')
    print('[tests] Image successfully deepfried. Saved at `./test/gradient-fried.jpg`.')

    with open('./tests/token.json') as t:
        data = json.load(t)

    print('[tests] Deepfrying `./test/test.jpg` with flares.')

    img = Image.open('./tests/human-test.jpg')
    img = await deeppyer.deepfry(img, token=data['token'], url_base=data.get('url_base', 'westcentralus'))

    img.save('./tests/human-fried.jpg')
    print('[tests] Human image successfully deepfried. Saved at `./test/human-fried`.')

    print('[tests] All tests successfully completed.')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())