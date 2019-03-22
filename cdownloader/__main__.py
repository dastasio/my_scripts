import sys
import os
import downloader as DL
import error_logging as DEBUG
import requests

if __name__ == "__main__":
    # obtaining url
    base_url = 'readcomiconline.to'
    urlToDownload = ''
    for arg in sys.argv:
        if base_url in arg:
            urlToDownload = arg
            break
    else:
        DEBUG.exitWithError("no 'readcomiconline.to' url specified")

    # getting url info
    clean_url = urlToDownload.replace('https://', '').replace('http://', '').replace('readcomiconline.to/', '')
    ## clean_url structure: "Comic/{Comic title}/{Issue number}"
    clean_url = clean_url.split('/')
    if not os.path.isdir('temp'):
        os.mkdir('temp')
    if len(clean_url) == 3 and clean_url[0] == 'Comic':
        # single-issue download
        DL.download_issue(urlToDownload)
    elif len(clean_url) == 2 and clean_url[0] == 'Comic':
        DL.manage_batch(urlToDownload)
    else:
        # 'Comic' not present in url: path is not a comic page
        os.removedirs('temp')
        DEBUG.exitWithError('the given url is not recognized as a comic')
    os.removedirs('temp')
    


    # guessing single chapter or batch
    '''slashes = url[domainCheck:].split('/')
    if len(slashes) == 3:
        1 == 1
        # batch
    elif len(slashes) == 4:
        # single
        title = slashes[2].replace('-', ' ')
        issue_number = slashes[3].replace('Issue-', '').replace('-', '.')
        out_dir = '{t} #{n}'.format(t=title, n=issue_number)
        #os.mkdir(out_dir)
        download_single_chapter(url, out_dir)'''
