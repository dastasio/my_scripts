from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import os
import time 
import bs4 as bs

def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollBy(0, 400);")

        # Wait to load the page.
        time.sleep(0.1)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

def GetEurobet():
    Events = []
    url = "https://www.eurobet.it/it/scommesse/#!/calcio/?  temporalFilter=TEMPORAL_FILTER_OGGI_DOMANI"

    driver = webdriver.Chrome()
    driver.set_window_size(1300, 800)
    driver.implicitly_wait(30)
    driver.get(url)
    scroll_down(driver)
    soup_level1=bs.BeautifulSoup(driver.page_source, 'lxml')
    events_source = soup_level1.find_all('div', 'event-row')
    driver.quit()
    for row in events_source:
        teams = row.find('div', 'event-players').span.find_all('span')
        quotas = row.find('div', 'event-wrapper-odds').find_all('div', 'group-quote-new')
        EventQuotes = []
        for quote in quotas:
            EventQuotes.append([float(v.string) for v in quote('a')])
        Event = [teams[0].string.strip(), teams[2].string.strip()]
        Event.extend(EventQuotes[0])
        Event.extend(EventQuotes[1])
        Events.append(Event)
    return Events

EUROBET_TEAM1 = 0
EUROBET_TEAM2 = 1
EUROBET_1 = 2
EUROBET_X = 3
EUROBET_2 = 4
EUROBET_UN25 = 5
EUROBET_OV25 = 6
EurobetEvents = GetEurobet()
data = open('data', 'w')