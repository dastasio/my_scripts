import sys
import os
from downloader import download_single_chapter

url = "https://readcomiconline.to/Comic/Marvel-Super-Heroes/Issue-13"

if __name__ == "__main__":
    # checking if given url is from readcomiconline.to
    domainCheck = url.find('readcomiconline.to')
    if domainCheck == -1:
        sys.exit("Error: given url is not recognized!")
    
    # guessing single chapter or batch
    slashes = url[domainCheck:].split('/')
    if len(slashes) == 3:
        1 == 1
        # batch
    elif len(slashes) == 4:
        # single
        title = slashes[2].replace('-', ' ')
        issue_number = slashes[3].replace('Issue-', '').replace('-', '.')
        out_dir = '{t} #{n}'.format(t=title, n=issue_number)
        #os.mkdir(out_dir)
        download_single_chapter(url, out_dir)
