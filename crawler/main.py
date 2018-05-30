from bs4 import BeautifulSoup
import requests
from settings import settings
from table import game_table

setting = settings()

def get_robots_txt(link, setting):
    page_response = requests.get(link)
    soup = BeautifulSoup(page_response.content, "html.parser")
    content = str(soup).split('\n')
    token = False
    for x in content:
        if('Crawl-delay' in x):
            setting.set_delay(int(" ".join(filter(str.isdigit, x))))
        elif(x and token):
            setting.add_to_denyList(x.split("Disallow: ")[1])
        elif(not x and token):
            token = False
        elif(x=="User-agent: *"):
            token = True
    setting.crawl_delay()

def get_game_scores(link, setting):
    if(setting.in_deny_list(link)):
        return
    page_response = requests.get(link)
    soup = BeautifulSoup(page_response.content, "html.parser")
    game = game_table()
    game.set_date('03/23/2018')
    headers = soup.find_all('div', class_ = 'section_heading')
    for header in headers:
        h2s = header.find_all('h2')
        for h2 in h2s:
            if('(' in h2.get_text()): #only get team names
                game.add_name(h2.get_text())
    rows = soup.find_all('tr')
    for row in rows:
        datarow = []
        theader = row.find_all('th')
        for th in theader:
            datarow.append(th.get_text())
        tdata = row.find_all('td')
        for tdatum in tdata:
            datarow.append(tdatum.get_text())
        game.add_row(datarow)
    game.table_to_csv()
    setting.crawl_delay()

get_robots_txt('https://www.basketball-reference.com/robots.txt', setting)
get_game_scores('https://www.basketball-reference.com/boxscores/201803230CHI.html', setting)