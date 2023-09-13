import time

from bs4 import BeautifulSoup
import requests
import csv

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
        scrapped_league_data = scrap_url(html.text)
        persist_transfer_data(scrapped_league_data)
        season = season + 1
        print('\n NEW NEW NEW NEW \n')
        time.sleep(5)


def scrap_url(html_content):
    league_transfers = []
    soup = BeautifulSoup(html_content, features='lxml')
    boxes = soup.find_all('h2', class_='content-box-headline content-box-headline--inverted content-box-headline--logo')
    transfer_season_tag = soup.find('h1', class_='content-box-headline').text.split()
    transfer_season = transfer_season_tag[1]
    for box in boxes:
        player_club = box.text
        tables = box.find_next_siblings('div', class_='responsive-table')
        joined_table_rows = tables[0].tbody.find_all('tr')
        for tr in joined_table_rows:
            player_name = tr.find('span').text
            player_age = tr.find('td', class_='zentriert alter-transfer-cell').text
            player_pos = tr.find('td', class_='pos-transfer-cell').text
            player_mv = tr.find('td', class_='rechts mw-transfer-cell').text
            player_left = tr.find('td', class_='no-border-links verein-flagge-transfer-cell').a.text
            player_transfer_fee_tags = tr.find_all('td', class_='rechts')
            player_transfer_fee = player_transfer_fee_tags[1].text
            transfer = Transfer(transfer_season, player_name, player_age, player_pos, player_club, player_left,
                                player_mv, player_transfer_fee)
            league_transfers.append(transfer)

        left_table_rows = tables[1].tbody.find_all('tr')
        for tr in left_table_rows:
            player_name = tr.find('span').text
            player_age = tr.find('td', class_='zentriert alter-transfer-cell').text
            player_pos = tr.find('td', class_='pos-transfer-cell').text
            player_mv = tr.find('td', class_='rechts mw-transfer-cell').text
            player_join_tags = tr.find('td', class_='no-border-links verein-flagge-transfer-cell').text
            player_join = player_join_tags.strip()
            player_transfer_fee_tags = tr.find_all('td', class_='rechts')
            player_transfer_fee = player_transfer_fee_tags[1].text
            transfer = Transfer(transfer_season, player_name, player_age, player_pos, player_join, player_club,
                                player_mv, player_transfer_fee)
            league_transfers.append(transfer)
    return league_transfers


def persist_transfer_data(transfers):
    with open('../data/transfers.csv', 'w') as csv_table:
        writer = csv.writer(csv_table)
        header = ['Season', 'Player', 'Age', 'Pos', 'Joined', 'Left', 'MV', 'Fee']
        writer.writerow(header)
        for transfer in transfers:
            formatted_transfer = transfer.__str__().split('#')
            writer.writerow(formatted_transfer)


get_urls(START_SEASON, LEAGUE)
