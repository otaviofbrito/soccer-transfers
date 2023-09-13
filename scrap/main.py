import time

from bs4 import BeautifulSoup
import requests

from scrap.domain.Transfer import Transfer

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

LEAGUE = 'GB1'
START_SEASON = 2022
END_SEASON = 2023




def get_urls(season, league):
    while season < END_SEASON:
        url = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/' + league + '/plus/?saison_id=' \
              + str(season) + '&s_w=&leihe=1&intern=0&intern=1'
        html = requests.get(url, headers=headers)
        scrap_url(html.text)
        season = season + 1
        print('\n NEW NEW NEW NEW \n')
        time.sleep(5)

def scrap_url(html_content):
    soup = BeautifulSoup(html_content, features='lxml')
    boxes = soup.find_all('h2', class_='content-box-headline content-box-headline--inverted content-box-headline--logo')
    transfer_season_tag = soup.find('h1', class_='content-box-headline').text.split()
    transfer_season = transfer_season_tag[1]
    for box in boxes:
        player_club = box.text
        joined_table = box.find_next_sibling('div', class_='responsive-table').tbody
        joined_table_rows = joined_table.find_all('tr')
        for tr in joined_table_rows:
            player_name = tr.find('span').text
            player_age = tr.find('td', class_='zentriert alter-transfer-cell').text
            player_pos = tr.find('td', class_='pos-transfer-cell').text
            player_mv = tr.find('td', class_='rechts mw-transfer-cell').text
            player_left = tr.find('td', class_='no-border-links verein-flagge-transfer-cell').a.text
            player_transfer_fee_tags = tr.find_all('td', class_='rechts')
            player_transfer_fee = player_transfer_fee_tags[1].text




get_urls(START_SEASON, LEAGUE)
