import glob
import fileinput
import re
import sys
import os

HTMLFilenames = glob.glob('./**/messages*.html', recursive=True)
LastChatID = ''
for Filename in HTMLFilenames:
    CurrentChatID = re.findall(r'chat_[0-9]+', Filename)[0]
    if CurrentChatID != LastChatID:
        LastChatID = CurrentChatID
        print('\rProcessing {}...'.format(CurrentChatID), end='')

    Data = 0
    with open(Filename, 'rb') as File:
        Data = File.read()
    
    Data, NumberOfSubs = re.subn(b'_thumb \(\d+?\)\.webp', b'_thumb.webp', Data)

    if NumberOfSubs > 0:
        with open(Filename, 'wb') as File:
            File.write(Data)

print('\nDeleting duplicate thumbnails')
ThumbFilenames = glob.glob('./**/stickers/*_thumb (*).webp', recursive=True)
for Filename in ThumbFilenames:
    os.remove(Filename)