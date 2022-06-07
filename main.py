import requests
from bs4 import BeautifulSoup
import sqlite3
import re
con = sqlite3.connect('example.db')
cur = con.cursor()

# Create table
try: 
    cur.execute('''CREATE TABLE movies
               (title text,rating real, popularity int)''')
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
    cur.execute("insert into movies values (?,?,?)",(title,rating,(cnt+1)))
    con.commit()
    filmlink = x.div.get("data-target-link")
    movielink = "https://letterboxd.com/esi" + filmlink + "stats/"
    moviestat = requests.get("https://letterboxd.com/esi" + filmlink + "stats/")
    print(f"Querying {movielink}")
    print(moviestat.content)
    likes = re.search(r'Liked by ([0-9].*)&nbsp', str(moviestat.content))
    likes = int(likes.group(1).replace(',',''))
    print(likes)
    print(filmlink)
con.close()
with open("yeah.html","w") as f:
    f.write(str(site.content))
