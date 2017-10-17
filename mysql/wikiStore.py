from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
try:
    cur.execute('CREATE DATABASE wiki_test')
except pymysql.err.ProgrammingError as e:
    print('MYSQL ERROR: ',e)
    if e.args[0] == 1007:
        print('数据库已存在！无需再次创建。')
cur.execute('USE wiki_test')
try:
    cur.execute('CREATE TABLE pages (id BIGINT(7) NOT NULL AUTO_INCREMENT, title VARCHAR(200),\
                content VARCHAR(10000), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id))')
except pymysql.err.InternalError as e:
    print('MYSQL ERROR: ', e)
    if e.args[0] == 1050:
        print('数据表已存在！无需再次创建。')
cur.execute('ALTER DATABASE wiki_test CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci')
cur.execute('ALTER TABLE pages CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE pages CHANGE title title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
cur.execute('ALTER TABLE pages CHANGE content content VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute('INSERT INTO pages (title, content) VALUES (\"%s\", \"%s\")', (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org'+articleUrl)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').get_text()
    content = soup.find('div', {'id':'mw-content-text'}).find('p').get_text()
    store(title, content)
    return soup.find('div', {'id':'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/kevin_Bacon')
try:
    while len(links)>0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        #print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()
