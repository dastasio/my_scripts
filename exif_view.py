import PIL.ExifTags
import PIL.Image
from os import listdir
from os.path import isfile, join, splitext

IMAGE_EXTENSIONS = ['.jpg', '.png']

imageList = []

for filename in listdir():
    if isfile(join('.', filename)):
        f, ext = splitext(filename)
        if ext.lower() in IMAGE_EXTENSIONS:
            imageList.append(filename)

for img in imageList:
    with PIL.Image.open(join('.', img)) as image:
        tags = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in image._getexif().items()
            if k in PIL.ExifTags.TAGS and PIL.ExifTags.TAGS[k] not in ['MakerNote', 'ImageDescription']
        }
        print(img)
        for tag in tags:
            print('\t' + str(tag) + ':\t' + str(tags[tag]))
        print("")