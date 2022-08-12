# Update all local href's from an HTML page into Google Drive links
# according to the content of an SQLite DB

import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

page = './index.htm'
db   = r'./links.db'
base = 'tdb'

try:
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    with open(page) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        for a in soup.find_all('a', href=True):
            h = a.get('href')
            if (not h.startswith('http://') and not h.startswith('#')):
                cursor.execute("SELECT url FROM links WHERE path='%s/%s';" % (base , h))
                record = cursor.fetchone()
                if record is None:
                    a['href'] = "!!BROKEN LINK!! (was \'%s\')" % h
                else:
                    a['href'] = record[0]
        print(str(soup))

    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if connection:
        connection.close()
