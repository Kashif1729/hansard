# import libraries
import urllib2
from bs4 import BeautifulSoup
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

def getOldContribs(searchTerm):

    contributionDates = []
    uniqueCounts = []

    # search archive dating from 1803-2005

    pageNum=1
    initURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(pageNum)+"sort=date&type=Commons"
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    totalPages = int(math.ceil(int(initSoup.find("h3", {"id": "results-header"}).getText().replace(',','').split()[-1])/10))

    for i in range(1,totalPages+1):

        print "Parsing archived page ", i, " of ", totalPages

        searchURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(i)+"sort=date&type=Commons"
        searchPage = urllib2.urlopen(searchURL).read()
        searchSoup = BeautifulSoup(searchPage,'lxml')
        resultHeadings = searchSoup.find_all("div", {"class": "date"})

        for result in resultHeadings:
            contribDate = result.getText().replace(',','').encode('utf-8').split()[2:5]
            contribDate[0] = str(datetime.strptime(contribDate[0], '%B').month)
            contribDateFormat = datetime.strptime(" ".join(contribDate), '%m %d %Y')
            contributionDates.append(contribDateFormat)

    uniqueDates = sorted(set(contributionDates))

    for date in uniqueDates:
        uniqueCounts.append(contributionDates.count(date))

    return uniqueDates, uniqueCounts

def getNewContribs(searchTerm,contributionDates,contributionCounts):

    # search new records from 2006-present day

    pageNum=1
    initURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(pageNum)
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    totalPages = int(initSoup.find("p", {"class": "pagination-total"}).getText().replace(',','').replace('(','').replace(')','').split()[-1])
    print totalPages

def plotContribs(searchTerm,uniqueDates,uniqueCounts):

    matplotlib.rcParams['toolbar'] = 'None' # switch off toolbar
    plt.plot(uniqueDates,uniqueCounts)
    plt.gcf().autofmt_xdate()
    plt.show()

# [dates, contributions] = getOldContribs("internet")

# search new records from 2006-present day

searchTerm = "India"

pageNum=1
contributionDates = []

initURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(pageNum)
initPage = urllib2.urlopen(initURL).read()
initSoup = BeautifulSoup(initPage,'lxml')

totalPages = int(initSoup.find("p", {"class": "pagination-total"}).getText().replace(',','').replace('(','').replace(')','').split()[-1])
print totalPages

for i in range(1,totalPages+1):

    print "Parsing archived page ", i, " of ", totalPages

    searchURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(i)+"sort=date&type=Commons"
    searchPage = urllib2.urlopen(searchURL).read()
    searchSoup = BeautifulSoup(searchPage,'lxml')
    resultHeadings = searchSoup.find_all("div", {"class": "date"})

    for result in resultHeadings:
        contribDate = result.getText().replace(',','').encode('utf-8').split()[2:5]
        contribDate[0] = str(datetime.strptime(contribDate[0], '%B').month)
        contribDateFormat = datetime.strptime(" ".join(contribDate), '%m %d %Y')
        contributionDates.append(contribDateFormat)