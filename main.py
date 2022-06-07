import requests
from bs4 import BeautifulSoup
import sqlite3
import re
con = sqlite3.connect('example.db')
cur = con.cursor()

# Create table
try: 
    cur.execute('''CREATE TABLE movies
               (title text,rating real, top250 int, likes int, watches int, lists int)''')
    con.commit()
except sqlite3.OperationalError:
    print("table already created")

site = requests.get("https://letterboxd.com/films/ajax/popular/size/small/?esiAllowFilters=true")
soup = BeautifulSoup(site.content, 'html.parser')
ratinglist = soup.find_all("li")
for cnt, x in enumerate(ratinglist):
    rating = x.get("data-average-rating")
    img = x.find('img')
    title = img.get('alt')
    filmlink = x.div.get("data-target-link")
    movielink = "https://letterboxd.com/esi" + filmlink + "stats/"
    moviestat = requests.get("https://letterboxd.com/esi" + filmlink + "stats/")
    print(f"Querying {movielink}")
    print(moviestat.content)
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
    cur.execute("insert into movies values (?,?,?)",(title,rating,toprating,likes,watches,lists))
    con.commit()
con.close()
with open("yeah.html","w") as f:
    f.write(str(site.content))
