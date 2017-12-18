# import libraries
import urllib2
from bs4 import BeautifulSoup
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

def getOldContribs(searchTerm):

    contributionDates = []

    # search archive dating from 1803-2005

    pageNum=1
    initURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(pageNum)+"sort=date&type=Commons"
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    if initSoup.find("p", {"class": "pagination-total"}):

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

    return contributionDates

def getNewContribs(searchTerm,contributionDates):

    # search new records from 2006-present day

    pageNum=1

    initURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(pageNum)
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    if initSoup.find("p", {"class": "pagination-total"}):

        totalPages = int(initSoup.find("p", {"class": "pagination-total"}).getText().replace(',','').replace('(','').replace(')','').split()[-1])

        for i in range(1,totalPages+1):

            print "Parsing new page ", i, " of ", totalPages

            searchURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(pageNum)
            searchPage = urllib2.urlopen(searchURL).read()
            searchSoup = BeautifulSoup(searchPage,'lxml')
            resultHeadings = searchSoup.find_all("div", {"class": "information with-portcullis clearfix"})

            for result in resultHeadings:
                contribDate = result.find_all("div")[1].getText().encode('utf-8').split()
                contribDate[1] = str(datetime.strptime(contribDate[1], '%B').month)
                contribDateFormat = datetime.strptime(" ".join(contribDate), '%d %m %Y')
                contributionDates.append(contribDateFormat)

    return contributionDates

def plotContribs(searchTerm,contributionDates):

    len(contributionDates)
    uniqueDates = sorted(set(contributionDates))
    uniqueCounts = []

    for date in uniqueDates:
        uniqueCounts.append(contributionDates.count(date))

    matplotlib.rcParams['toolbar'] = 'None' # switch off toolbar
    plt.bar(uniqueDates,uniqueCounts)
    plt.gcf().autofmt_xdate()
    plt.show()

    return uniqueDates, uniqueCounts

searchTerm = "meme"
contributionDates = getOldContribs(searchTerm)
contributionDates = getNewContribs(searchTerm,contributionDates)
[uniqueDates, uniqueCounts] = plotContribs(searchTerm,contributionDates)