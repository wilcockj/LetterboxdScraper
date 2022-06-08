import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import random
import time
con = sqlite3.connect('movies.db')
cur = con.cursor()

# Create table
def gatherandstoredata(site):
    site = requests.get(site)
    soup = BeautifulSoup(site.content, 'html.parser')
    ratinglist = soup.find_all("li")
    for x in ratinglist:
        rating = x.get("data-average-rating")
        img = x.find('img')
        title = img.get('alt')
        filmlink = x.div.get("data-target-link")
        movielink = "https://letterboxd.com/esi" + filmlink + "stats/"
        moviestat = requests.get("https://letterboxd.com/esi" + filmlink + "stats/")
        #print(f"Querying {movielink}")
        #print(moviestat.content)
        likes = re.search(r'Liked by ([0-9].*?)&nbsp', str(moviestat.content))
        likes = likes.group(1)#int(likes.group(1).replace(',',''))
        likes = int(likes.replace(',',''))
        watches = re.search(r'Watched by ([0-9].*?)&nbsp', str(moviestat.content))
        watches = watches.group(1)
        watches = int(watches.replace(',',''))
        lists = re.search(r'Appears in ([0-9].*?)&nbsp', str(moviestat.content))
        lists = lists.group(1)
        lists = lists.replace(',','')


        toprating = re.search(r'([0-9]{1,3}) in the Letterboxd',str(moviestat.content))
        if toprating:
            toprating = int(toprating.group(1))
        else:
            toprating = 0
        '''
        print(likes)
        print(watches)
        print(lists)
        print(toprating)
        print(filmlink)
        '''
        try:
            cur.execute("insert into movies values (?,?,?,?,?,?,?)",(title,rating,toprating,likes,watches,lists,filmlink))
            con.commit()
        except sqlite3.IntegrityError:
            print(f"already have data on {title}")
        time.sleep(random.randint(3,9))
if __name__ == '__main__':
    try: 
        cur.execute('''CREATE TABLE movies
                   (title text,rating real, top250 int, likes int, watches int, lists int,link text unique)''')
        con.commit()
    except sqlite3.OperationalError:
        print("table already created")

    for x in range(100):
        print(f"Gathering data on page {x}")
        gatherandstoredata("https://letterboxd.com/films/ajax/popular/size/small/page/" + str(x) + "/")
    con.close()
