#!/usr/bin/python3

import json
import requests
import re
from bs4 import BeautifulSoup
from more_itertools import unique_everseen


# Scrap show title
def scrap_show_title(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.select('.b-serial-highlight h2.title')[0].text.strip()
    return title


# Scrap all available seasons from JOJ show
def scrap_seasons(url):
    # Scraping seasons (get ids from list)
    print('---> Scraping seasons: ', end='');
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    id_options = soup.select('.e-select select option')
    seasons = []
    for id_option in id_options:
        seasons.append(
            {
                'id': id_option.attrs.get('value'),
                'label': id_option.text.strip()
            }
        )
    # Correct seasons order
    seasons = list(reversed(seasons))
    print(len(seasons), 'seasons found');
    return seasons


# Scraping episodes from season
def scrap_episodes_from_season(season, url):
    links = []
    season_url = url + '?seasonId=' + season.get('id')
    while True:
        print('.', end='', flush=True)
        page = requests.get(season_url).text
        soup = BeautifulSoup(page, 'html.parser')

        links_data = soup.select('.e-mobile-article-p.scroll article a')
        for link_data in links_data:
            link = link_data.attrs.get('href')
            if '/inkognito/epizoda' not in link:
                continue
            links.append(link)

        more_link = soup.find('a', {'title': 'Načítaj viac'})
        if more_link:
            season_url = base_url + more_link.attrs.get('href')
        else:
            season_url = False

        if season_url:
            continue
        else:
            break

    links = list(unique_everseen(links))
    return links


def scrap_episode(episode_url):
    print('.', end='', flush=True)
    page = requests.get(episode_url).text
    soup = BeautifulSoup(page, 'html.parser')
    episode_title = soup.select('.b-video-title h2.title')
    episode_data = {
        'episode': episode_title[0].text.strip() if episode_title else episode_url,
        'videoLinks': {}
    }

    iframe = soup.select('.s-video-detail .s-fullwidth-mobile iframe')
    if iframe:
        page = requests.get(iframe[0].attrs.get('src')).text
        match_360 = re.search(re_360_mp4, page)
        match_540 = re.search(re_540_mp4, page)
        match_720 = re.search(re_720_mp4, page)

        episode_data['videoLinks'] = {
            '360p': match_360.group(1) if match_360 else None,
            '540p': match_540.group(1) if match_540 else None,
            '720p': match_720.group(1) if match_720 else None,
        }
    else:
        episode_data['videoLinks'] = None
    return episode_data


# Settings for show
base_url = 'https://videoportal.joj.sk'
url = base_url + '/inkognito'
re_360_mp4 = re.compile(r"'(https:\/\/[^']+(?:360|360p)\.mp4)'")
re_540_mp4 = re.compile(r"'(https:\/\/[^']+(?:540|540p)\.mp4)'")
re_720_mp4 = re.compile(r"'(https:\/\/[^']+(?:720|720p)\.mp4)'")
show_title = scrap_show_title(url)

print('---> Begin scrapping show:', show_title)

# Empty dictionary
show = []

# Scrap seasons
show_seasons = scrap_seasons(url)
for season in show_seasons:
    season_data = {
        'season': season.get('label'),
        'episodes': []
    }

    print('---> Scrap season:', season.get('label'), '[', end='', flush=True)
    episodes = scrap_episodes_from_season(season, url)
    print('] Scraped', len(episodes), 'episodes')
    print('     Scrap video_links for episodes [', end='', flush=True)
    for episode_url in list(reversed(episodes)):
        season_data['episodes'].append(scrap_episode(episode_url))
    print(']')
    show.append(season_data)

print('---> Write scrapped data as JSON')
with open('inkognito.json', 'w', encoding='utf-8') as outfile:
    json.dump(show, outfile, indent=2, ensure_ascii=False, separators=(',', ': '))