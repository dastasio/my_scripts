import piexif
import glob

Filenames = glob.glob('./*.jpg')
#for Filename in Filenames:
print(Filenames[0])
for Filename in Filenames:
    print("Processing", Filename, end='\r')
    ImageDataFromName = Filename[2:-4].split('-')
    Year = ImageDataFromName[1][:4]
    Month = ImageDataFromName[1][4:6]
    Day = ImageDataFromName[1][6:8]

    Seconds = int(ImageDataFromName[2][2:])*5
    Hours = int(Seconds/3600)
    Seconds = Seconds % 3600
    Minutes = int(Seconds/60)
    Seconds = Seconds % 60
    OriginalDate = u"{y}:{M}:{d} {h}:{m}:{s}".format(y=Year, M=Month, d=Day, h=Hours, m=Minutes,    s=Seconds)

    ExifData = piexif.load(Filename)

    ExifData['Exif'] = {piexif.ExifIFD.DateTimeOriginal: OriginalDate}
    ExifBytes = piexif.dump(ExifData)
    piexif.insert(ExifBytes, Filename)