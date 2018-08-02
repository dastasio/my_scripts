import cfscrape
import requests
import shutil
import zipfile
import os


def get_page_html(url):
    scraper = cfscrape.create_scraper(delay=10)
    cookies = {'rco_readType':'1', 'rco_quality':'hq'}
    return scraper.get(url, cookies=cookies).content.decode('utf-8')


def download_single_chapter(url, path):
    source = get_page_html(url)
    start = source.find('lstImages.push(')
    lastCall = source.rfind('lstImages.push(')
    end = lastCall + source[lastCall:].find(';') + 1

    pagelinks = source[start:end].replace(' ', '').replace('lstImages.push("', '').replace('");', '').split(os.linesep)
    pagelinks = [x for x in pagelinks if x]
    
    count = 0
    out_cbz = zipfile.ZipFile(path + '.cbz', 'w')
    for page in pagelinks:
        download_page(page, count, out_cbz)
        count = count + 1
    out_cbz.close()

def download_page(page_url, page_number, cbz_file):
    res = requests.get(page_url, stream=True)
    with open(str(page_number) + '.jpeg', 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    cbz_file.write(str(page_number) + '.jpeg')
    os.remove(str(page_number) + '.jpeg')