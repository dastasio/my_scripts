import cfscrape
import json
import urllib.request
import time
import subprocess
from os import replace, path
from bs4 import BeautifulSoup

def get_page_html(url):
    #response = urllib.request.urlopen(url)
    #return response.read()
    scraper = cfscrape.create_scraper()
    return scraper.get(url).content

def download_mp4(url, filename, title):
    urllib.request.urlretrieve(url, filename)
    cmd = 'ffmpeg -i "' + filename + '" -y -codec copy -metadata title="' + title + '" "' + filename + 'edit.mp4"'
    subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    replace(filename + 'edit.mp4', filename)

def tiktok(url):
    soup = BeautifulSoup(get_page_html(url), 'html.parser')
    title = soup.head.title
    metadata = json.loads(soup.find('script', id='videoObject').string)
    video_date  = metadata['uploadDate']
    video_date = time.strptime(video_date.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    video_date = time.strftime('%Y-%m-%d_%H-%M-%S', video_date)
    video_title = metadata['name'].split('on TikTok')[1].lstrip()
    video_url   = metadata['contentUrl']
    print(video_date)
    filename = 'out/' + video_date + '.mp4'
    if not path.exists(filename):
        download_mp4(video_url, filename, video_title)

def get_all_video_urls_from_user(html):
    urls = []
    soup = BeautifulSoup(html, 'html.parser')
    video_tags = soup.find_all('a', attrs={'class' : 'jsx-2810521537 video-feed-item-wrapper'})
    for tag in video_tags:
        urls.append(tag['href'])
    return urls

if __name__ == '__main__':
    in_html = open(path_to_html, 'r', encoding='utf-8')
    urls = get_all_video_urls_from_user(in_html.read())
    errors = []

    with open('error.log', 'w') as errors:
        for i in range(len(urls)):
            try:
                print('Downloading ' + str(i+1) + ' out of ' + str(len(urls)) + ': ', end='')
                tiktok(urls[i])
            except:
                errors.write(str(i) + ': ')
                errors.write(urls[i])
                errors.write('\n')
                print('error')
