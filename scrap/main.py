import time

from bs4 import BeautifulSoup
import requests
import csv

from scrap.domain.Transfer import Transfer

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

LEAGUES = ['BRA1', 'GB1', 'IT1', 'ES1', 'L1', 'FR1', 'TR1', 'SA1', 'JAP1', 'CSL', 'UAE1', 'RSK1', 'QSL',
           'IRN1', 'IN1L', 'GR1', 'KR1', 'TS1', 'DK1', 'SER1', 'RO1', 'SE1', 'UNG1', 'ZYP1', 'BU1', 'MLS1', 'CDN1']
START_SEASON = 1992
END_SEASON = 2023
TABLE_FILE = "new_table.csv"


def create_table(file):
    with open('../data/' + str(file), 'w') as csv_table:
        writer = csv.writer(csv_table)
        header = ['Season', 'Player', 'Age', 'Pos', 'Joined', 'Left', 'MV', 'Fee']
        writer.writerow(header)


def get_urls(season, leagues):
    while season < END_SEASON:
        for lg in leagues:
            url = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/' + lg + '/plus/?saison_id=' \
                  + str(season) + '&s_w=&leihe=1&intern=0&intern=1'
            try:
                print("Trying to fetch: " + url)
                html = requests.get(url, headers=headers)
                print("Connection success, status code: " + str(html.status_code))
            except requests.exceptions.RequestException as err:
                print("\nAn error occurred with the request: ")
                print(err)

            scrapped_league_data = scrap_url(html.text)
            try:
                data_len = len(scrapped_league_data)
                if data_len > 0:
                    Transfer.persist_transfer_data(scrapped_league_data, TABLE_FILE)
                    print('\n' + str(data_len) + ' transfers were stored')
                else:
                    print("No data stored")
            except Exception:
                print("No data stored")

            print('\nFetching next url... \n')

        season = season + 1


def scrap_url(html_content):
    try:
        league_transfers = []
        soup = BeautifulSoup(html_content, features='lxml')
        boxes = soup.find_all('h2',
                              class_='content-box-headline content-box-headline--inverted content-box-headline--logo')
        transfer_season_tag = soup.find('h1', class_='content-box-headline').text.split()
        transfer_season = transfer_season_tag[1]
        for box in boxes:
            player_club = box.text.strip()
            tables = box.find_next_siblings('div', class_='responsive-table')
            for table in tables:
                try:
                    transfer_action = table.thead.find('th', class_='spieler-transfer-cell').text.lower()
                    transfer_table_rows = table.tbody.find_all('tr')
                    for ttr in transfer_table_rows:
                        player_name = ttr.find('span').text
                        player_age = ttr.find('td', class_='zentriert alter-transfer-cell').text
                        player_pos = ttr.find('td', class_='pos-transfer-cell').text
                        player_mv = ttr.find('td', class_='rechts mw-transfer-cell').text
                        player_move_action_tags = ttr.find('td',
                                                           class_='no-border-links verein-flagge-transfer-cell').text
                        player_move_action = player_move_action_tags.strip()
                        player_transfer_fee_tags = ttr.find_all('td', class_='rechts')
                        player_transfer_fee = player_transfer_fee_tags[1].text
                        if "End of loan" in player_transfer_fee:
                            player_transfer_fee = player_transfer_fee.replace('End of loan', 'End of loan: ')

                        if transfer_action == 'in':
                            transfer = Transfer(transfer_season, player_name, player_age, player_pos, player_club,
                                                player_move_action, player_mv, player_transfer_fee)
                            league_transfers.append(transfer)
                        elif transfer_action == 'out':
                            transfer = Transfer(transfer_season, player_name, player_age, player_pos,
                                                player_move_action, player_club, player_mv, player_transfer_fee)
                            league_transfers.append(transfer)
                except AttributeError:
                    pass
        return league_transfers
    except Exception:
        print("HTML is empty of useful data")


def main():
    create_table(TABLE_FILE)
    get_urls(START_SEASON, LEAGUES)


if __name__ == "__main__":
    main()
