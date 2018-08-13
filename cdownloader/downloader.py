import cfscrape
import requests
import shutil
import zipfile
import os
import sys
import error_logging as DEBUG

FILENAME_CLEANER = {'/': '-', '\\' : '-', ':' : ','}

def get_page_html(url):
    scraper = cfscrape.create_scraper(delay=10)
    cookies = {'rco_readType':'1', 'rco_quality':'hq'}
    return scraper.get(url, cookies=cookies).content.decode('utf-8')


def download_issue(url, path = './', comicName = '', issueNumber = -1):
    source = get_page_html(url)

    # TODO: fix title finding algorithm
    # if function was called by a batch download, 'comicName' and 'issueNumber' are populated
    # if they are void, we proceed with finding them
    if not comicName and issueNumber == -1:
        # getting comic name
        titleTagStartIndex = source.find('<title>') + 7
        titleTagEndIndex = source.find('</title>')
        titleTag = source[titleTagStartIndex : titleTagEndIndex].lstrip()
        titleEndIndex = -1
        if 'Issue' in titleTag:
            titleEndIndex = titleTag.find('Issue')
        elif 'Full' in titleTag:
            titleEndIndex = titleTag.find('Full')
        elif 'TPB' in titleTag:
            titleEndIndex = titleTag.find('TPB')
        
        if titleEndIndex == -1:
            DEBUG.exitWithError('Could not determine single-issue title')
        comicName = titleTag[:titleEndIndex].rstrip()

        # getting issue number
        issueNumberStartIndex = titleTag.find(comicName) + len(comicName)
        issueNumberEndIndex = titleTag.find('- Read')
        if issueNumberEndIndex == -1:
            issueNumberEndIndex = titleTag.find('| Read')
        issueNumber = titleTag[issueNumberStartIndex : issueNumberEndIndex].lstrip().rstrip().replace('Issue ', '')
    # cleaning forbidden characters in filenames
    for token in FILENAME_CLEANER:
        comicName = comicName.replace(token, FILENAME_CLEANER[token])
    
    if path == './':
        path += comicName + issueNumber
    # downloading issue
    start = source.find('lstImages.push(')
    lastCall = source.rfind('lstImages.push(')
    end = lastCall + source[lastCall:].find(';') + 1

    pagelinks = source[start:end].replace(' ', '').replace('lstImages.push("', '').replace('");', '').split(os.linesep)
    pagelinks = [x for x in pagelinks if x]
    
    count = 1
    out_cbz = zipfile.ZipFile(path + '.cbz', 'w')
    for page in pagelinks:
        download_page(page, count, out_cbz)
        count = count + 1
    out_cbz.close()

def download_page(page_url, page_number, cbz_file):
    res = requests.get(page_url, stream=True)
    with open('temp/' + str(page_number) + '.jpeg', 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    cbz_file.write('temp/' + str(page_number) + '.jpeg')
    os.remove('temp/' + str(page_number) + '.jpeg')