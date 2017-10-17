from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict
import operator

def clearInput(input):
    input = input.lower()
    content = re.sub('\n+', ' ', input)
    content = re.sub('\[[0-9]*\]', '', content)
    content = re.sub(' +', ' ', content)
    content = bytes(content, 'utf-8')
    content = content.decode('ascii', 'ignore')
    output = []
    content = content.split(' ')
    for item in content:
        item = item.strip(string.punctuation)
        if len(item)>1 or (item.lower() == 'a') or (item.lower() == 'i'):
            output.append(item)
    return output

def ngrams(input, n):
    input = clearInput(input)
    output = {}
    for i in range(len(input)-n+1):
        temp = ' '.join(input[i:i+n])
        if temp not in output:
            output[temp] = 0
        output[temp] += 1
    return output

def isCommon(ngrams):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
                   "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
                   "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
                   "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
                   "if", "would", "her", "all", "my", "make", "about", "know", "will",
                   "as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take",
                   "out", "into", "just", "see", "him", "your", "come", "could", "now",
                   "than", "like", "other", "how", "then", "its", "our", "two", "more",
                   "these", "want", "way", "look", "first", "also", "new", "because",
                   "day", "more", "use", "no", "man", "find", "here", "thing", "give",
                   "many", "well"]
    for word in ngrams:
        if word in commonWords:
            return True
    return False

content = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
ngrams = ngrams(content, 2)
sortedNgrams = sorted(ngrams.items(), key=operator.itemgetter(1), reverse=True)
print(sortedNgrams)
print(len(sortedNgrams))
'''
soup = BeautifulSoup(html, 'lxml')
content = soup.find('div', {'id':'mw-content-text'}).get_text()
ngrams = ngrams(content, 2)
ngrams = OrderedDict(sorted(ngrams, key=lambda t:t[1], reverse=True))
print(ngrams)
print('2-grams count is: '+str(len(ngrams)))
'''