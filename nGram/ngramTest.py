from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string

def clearInput(input):
    content = re.sub('\n+', ' ', input)
    content = re.sub('\[[0-9]*\]', '', content)
    content = re.sub(' +', ' ', content)
    content = bytes(content, 'utf-8')
    content = content.decode('ascii', 'ignore')
    output = []
    content = content.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item)>1 or (item.lower() == 'a') or (item.lower() == 'i'):
            output.append(item)
    return output

def ngrams(input, n):
    input = clearInput(input)
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
soup = BeautifulSoup(html, 'lxml')
content = soup.find('div', {'id':'mw-content-text'}).get_text()
ngarms = ngrams(content, 2)
print(ngarms)
print('2-grams count is: '+str(len(ngarms)))