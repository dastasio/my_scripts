import cfscrape
import requests
import shutil
from os import linesep
url = "https://readcomiconline.to/Comic/Marvel-Super-Heroes/Issue-13"
page_count = 1


def get_page_html(url):
    scraper = cfscrape.create_scraper(delay=10)
    cookies = {'rco_readType':'1', 'rco_quality':'hq'}
    return scraper.get(url, cookies=cookies).content.decode('utf-8')



def download_single_chapter(url):
    source = get_page_html(url)
    start = source.find('lstImages.push(')
    lastCall = source.rfind('lstImages.push(')
    end = lastCall + source[lastCall:].find(';') + 1

    pagelinks = source[start:end].replace(' ', '').replace('lstImages.push("', '').replace('");', '').split(linesep)
    pagelinks = [x for x in pagelinks if x]
    
    count = 0
    for page in pagelinks:
        download_page(page, count)
        count = count + 1

def download_page(page_url, filename):
    res = requests.get(page_url, stream=True)
    with open('pages/{filename}.jpeg'.format(filename=filename), 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)

if __name__ == "__main__":
    download_single_chapter(url)