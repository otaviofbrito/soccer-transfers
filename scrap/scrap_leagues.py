from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

START_PAGE = 1
LAST_PAGE = 3  # DEFINE LAST PAGE


def get_url(current_pg, last_pg):
    leagues = []
    while current_pg <= last_pg:

        url = "https://www.transfermarkt.com/wettbewerbe/amerika/wettbewerbe?plus=1&page=" + str(current_pg)
        try:
            print("Trying to fetch: " + url)
            html = requests.get(url, headers=headers)
            print("Connection success, status code: " + str(html.status_code))

            print('Page: ' + str(current_pg) + '/' + str(last_pg))
            leagues_scrapped = scrap_league_tag(html.text)
            leagues = leagues + leagues_scrapped
            print(leagues)

        except requests.exceptions.RequestException as err:
            print("\nAn error occurred with the request: ")
            print(err)

        print('\nFetching next url... \n')
        current_pg = current_pg + 1

    return leagues


def scrap_league_tag(html_content):
    league_tags = []
    soup = BeautifulSoup(html_content, features='lxml')
    tag_div = soup.find('div', class_="keys")
    tags = tag_div.find_all('span')
    for tag in tags:
        league_tags.append(tag.text)

    return league_tags


def persist_league_data(leagues):
    with open("leagues_america.txt", "w") as file:
        for lg in leagues:
            file.write(lg)
            file.write('\n')


def scrap_leagues():
    leagues = get_url(START_PAGE, LAST_PAGE)
    persist_league_data(leagues)
    print(leagues)


if __name__ == "__main__":
    scrap_leagues()
