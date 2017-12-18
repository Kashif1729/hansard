# import libraries
import urllib2
from bs4 import BeautifulSoup
import math
from datetime import datetime
import collections

def getContribs(searchTerm):

    contributions = []

    pageNum=1
    initURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(pageNum)+"sort=date&type=Commons"
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    totalPages = int(math.ceil(int(initSoup.find("h3", {"id": "results-header"}).getText().replace(',','').split()[-1])/10))

    for i in range(1,totalPages+1):

        print "Parsing page ", i, " of ", totalPages

        searchURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(i)+"sort=date&type=Commons"
        searchPage = urllib2.urlopen(searchURL).read()
        searchSoup = BeautifulSoup(searchPage,'lxml')
        resultHeadings = searchSoup.find_all("div", {"class": "date"})

        for result in resultHeadings:
            contribDate = result.getText().replace(',','').encode('utf-8').split()[2:5]
            contribDateFormat = datetime.strptime(" ".join(contribDate), '%B %d %Y')
            contributions.append(contribDateFormat)

    return contributions

contributions = getContribs("Twitter")
ctr = collections.Counter(contributions)

print ctr