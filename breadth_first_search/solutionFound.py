from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE wiki_test')

class SolutionFound(RuntimeError):
    def __init__(self, message):
        self.message = message

    def getLinks(fromPageId):
        cur.execute('SELECT toPageId FROM links WHERE fromPageId=%s', (fromPageId))
        if cur.rowcount == 0:
            return None
        else:
            return [x[0] for x in cur.fetchall()]

    def constructDict(currentPageId):
        links = getLinks(currentPageId)
        if links:
            return dict(zip(links, [{}]*len(links)))
        else:
            return {}

    def searchDepth(targetPageId, currentPageId, linkTree, depth):
        if depth == 0:
            return linkTree
        if not linkTree:
            linkTree = constructDict(currentPageId)
            if not linkTree:
                return {}
        if targetPageId in linkTree.keys():
            print('Target ' +str(targetPageId)+ ' found!')
            raise SolutionFound('Page: '+str(currentPageId))

        for branchKey, branchValue in linkTree.items():
            try:
                linkTree[branchKey] = searchDepth(targetPageId, branchKey, branchValue, depth-1)
            except SolutionFound as e:
                print(e.message)
                raise SolutionFound('Page: ' +str(currentPageId)+ ' found!')
        return linkTree

    try:
        searchDepth(134951, 1, {}, 4)
        print('No solution found!')
    except SolutionFound as e:
        print(e.message)

