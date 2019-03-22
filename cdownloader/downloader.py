import cfscrape
import requests
import shutil
import zipfile
import os
import sys
import re
import error_logging as DEBUG

FILENAME_CLEANER = {'/': '-', '\\' : '-', ':' : ','}
session = requests.session()
session.cookies.update({'rco_readType':'1', 'rco_quality':'hq'})

def get_page_html(url):
    scraper = cfscrape.create_scraper(sess=session)
    return scraper.get(url).content.decode('utf-8')


def download_issue(url, path = './', comicName = '', issueNumber = -1):
    source = get_page_html(url)

    # TODO: fix title finding algorithm
    # if function was called by a batch download, 'comicName' and 'issueNumber' are populated
    # if they are void, we proceed with finding them
    if not comicName and issueNumber == -1:
        # getting comic name
        titleTagStartIndex = source.find('<title>') + 7
        titleTagEndIndex = source.find('</title>')
        titleTag = ' '.join(source[titleTagStartIndex : titleTagEndIndex].split())
        titleEndIndex = -1
        if 'Issue' in titleTag:
            titleEndIndex = titleTag.find('Issue')
        elif 'Annual' in titleTag:
            titleEndIndex = titleTag.find('Annual')
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
        issueNumber = titleTag[issueNumberStartIndex : issueNumberEndIndex].lstrip().rstrip().replace('Issue ', ' ')
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

def manage_batch(url, path = './', startIssue = -1, endIssue = -1):
    source = get_page_html(url)
    IssueListStart = source.find('<div class="heading"><h3>Issue(s)</h3></div>')
    IssueListStart = source.find('<li>', IssueListStart)
    IssueListEnd = source.find('</ul>', IssueListStart)
    IssueListEnd = source.rfind('</li>', 0, IssueListEnd)
    issues, annuals = get_issue_list(source[IssueListStart:IssueListEnd])
    
    if issues and annuals:
        print("Monthly and Annual issues found!")
    elif issues:
        print('Issue list found!')
    elif annuals:
        print('Annuals list found!')
    else:
        DEBUG.exitWithError("No list of issues found")
    selection = input('Enter range of issues to download: ')
    if not selection.replace('a', '').replace('i', '').replace('-', '').replace(',', '').replace('.', '').isdigit():
        DEBUG.exitWithError("Invalid range inserted")
    batches = selection.split(',')
    for batch in batches:
        if 'a' in batch.lower():
            batch = batch.lower().replace('a', '')
            extremes = batch.split('-')
            if len(extremes) == 1:
                pass # TODO
            else:
                if 'i' in extremes[0].lower() or 'i' in extremes[1].lower():
                    DEBUG.exitWithError("Error: you mixed monthly and annual releases in '" + batch + "'")
                for n in annuals:
                    number = re.findall('\d+\.\d+', n)
                    if float(extremes[0]) <= number <= float(extremes[1]):
                        download_issue(annuals[n])
                    elif number > float(extremes[1]):
                        break
        elif 'i' in batch.lower():
            batch = batch.lower().replace('i', '')
            extremes = batch.split('-')
            if len(extremes) == 1:
                pass # TODO
            else:
                if 'a' in extremes[0].lower() or 'a' in extremes[1].lower():
                    DEBUG.exitWithError("Error: you mixed monthly and annual releases in '" + batch + "'")
                for n in issues:
                    number = re.findall('\d+\.\d+', n)
                    if len(number) != 0:
                        number = float(number[0])
                    else:
                        number = float(re.findall('\d+', n)[0])
                    if float(extremes[0]) <= number <= float(extremes[1]):
                        download_issue(issues[n])
                    elif number > float(extremes[1]):
                        break
            

def get_issue_list(src):
    issuesSRC = [line.strip() for line in src.split(os.linesep) if line.strip()]
    issues = dict()
    annuals = dict()
    for item in reversed(issuesSRC):
        number = item[item.find('<span>') + 6 : item.find('</span>')]
        if 'Issue' in number:
            issues[number] = 'https://readcomiconline.to' + item[item.find('"') + 1: item.rfind('"')]
        elif 'Annual' in number:
            annuals[number] = 'https://readcomiconline.to' + item[item.find('"') + 1: item.rfind('"')]
    return issues, annuals

def download_batch(urls, path = './', startIssue = -1, endIssue = -1):
    with open('src.html', 'w') as f:
        for n in iter(urls):
            f.write(n + ': ' + urls[n] + '\n')

def download_page(page_url, page_number, cbz_file):
    print("Downloading page {p} for {f}".format(p=page_number, f=cbz_file))
    res = requests.get(page_url, stream=True)
    with open('temp/' + str(page_number) + '.jpeg', 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
    cbz_file.write('temp/' + str(page_number) + '.jpeg')
    os.remove('temp/' + str(page_number) + '.jpeg')