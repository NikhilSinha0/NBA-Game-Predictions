from bs4 import BeautifulSoup
import requests
from settings import settings
from table import game_table
from links import links
from datetime import datetime
from datetime import timedelta
from season import season
import time
import sys

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
    print("Got robots.txt")
    setting.crawl_delay()

def get_game_scores(link, date_string, setting, season):
    if(setting.in_deny_list(link)):
        return
    page_response = requests.get(link)
    soup = BeautifulSoup(page_response.content, "html.parser")
    game = game_table()
    game.set_date(date_string)
    headers = soup.find_all('div', class_ = 'section_heading')
    prev = soup.find_all(class_ = 'prev')
    prevs = []
    for item in prev:
        last_location = item['href'].split('.')[0][-3:]
        last_time = item['href'].split('/')[-1].split('.')[0][:-4]
        prevs.append([item.parent.parent.find_all('strong')[0].get_text().strip('\n'), last_location, last_time])
    for header in headers:
        h2s = header.find_all('h2')
        for h2 in h2s:
            if('(' in h2.get_text()): #only get team names
                game.add_name(h2.get_text())
    game.add_last_game_info(prevs)
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
    game.set_win_loss()
    game.sync_last_game_info(season)
    game.table_to_csv()
    game.table_to_json()
    setting.crawl_delay()

def get_game_links_from_date(date, setting, links):
    link = format_date_link(date)
    date_string = "/".join([str(x) for x in date])
    if(setting.in_deny_list(link)):
        return
    page_response = requests.get(link)
    soup = BeautifulSoup(page_response.content, "html.parser")
    next_day = soup.find_all(class_='next')
    if(len(next_day) < 1):
        print("Dropping date " + date_string)
        return None
    next_link = next_day[0]
    game_links = soup.find_all(class_ = 'gamelink')
    cleaned_game_links = [x.find_all('a')[0]['href'] for x in game_links]
    for game_link in cleaned_game_links:
        links.add_link(game_link, date_string)
    print("Got links for " + date_string)
    setting.crawl_delay()
    return next_link['href']

def scrape_by_dates(date1, date2, setting, links):
    d1 = [int(x) for x in date1.split('/')]
    d2 = [int(x) for x in date2.split('/')]
    while(datetime(d1[2], d1[0], d1[1]) <= datetime(d2[2], d2[0], d2[1])):
        next_link = get_game_links_from_date(d1, setting, links)
        if(next_link==None):
            print("Dropped a date, getting games until "+"/".join([str(x) for x in d1]))
            return
        d1 = extract_date_from_link(next_link)

def scrape_games_by_links(settings, links, season, return_jsons):
    if return_jsons:
        return #implement way to return json objects instead of writing to file
    while(links.has_links()):
        link, date = links.get_next_link()
        get_game_scores(link, date, settings, season)

def format_date_link(date):
    mm, dd, yy = [str(x) for x in date]
    return'https://www.basketball-reference.com/boxscores/?month='+mm+'&day='+dd+'&year='+yy

def extract_date_from_link(link):
    parts = link.split('&')
    mm, dd, yy = [int(part.split('=')[1]) for part in parts]
    return mm, dd, yy

def get_today():
    setting = settings()
    linksobj = links()
    seasonsobj = season()
    today = datetime.datetime.today()
    today_date = '/'.join([today.month, today.day, today.year])
    start_date, end_date = today_date, today_date
    get_robots_txt('https://www.basketball-reference.com/robots.txt', setting)
    scrape_by_dates(start_date, end_date, setting, linksobj)
    scrape_games_by_links(setting, linksobj, seasonsobj, True)

def main():
    setting = settings()
    linksobj = links()
    seasonsobj = season()
    args = sys.argv[1:]
    if(len(args)!=2):
        print("There should be exactly 2 arguments, the start and end date in MM/DD/YYYY")
        return
    print("\nDates will be output in YYYY/MM/DD for ordering purposes\n")
    start_date = args[0]
    end_date = args[1]
    start = time.time()
    get_robots_txt('https://www.basketball-reference.com/robots.txt', setting)
    scrape_by_dates(start_date, end_date, setting, linksobj)
    #linksobj.print_links()
    scrape_games_by_links(setting, linksobj, seasonsobj)
    end = time.time()
    print("Done. Time elapsed: " + str(timedelta(seconds = int(end - start))))

if(__name__=='__main__'):
    main()