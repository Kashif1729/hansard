# import libraries
import urllib2
import requests
from bs4 import BeautifulSoup
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import re

def getOldContribs(searchTerm):

    contributionDates = []

    # search archive dating from 1803-2005

    pageNum=1
    initURL = "http://hansard.millbanksystems.com/search/"+searchTerm+"?page="+str(pageNum)+"sort=date&type=Commons"
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    if initSoup.find("h3", {"id": "results-header"}):

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

def getMidContribs(searchTerm): # this is super gross

    contributionDates = []

    # search archive from 2005-2010

    days = ['01', '02', '03', '04', '05', '06', '07' ,'08' ,'09', '10', '11' ,'12', '13', '14' ,'15',
            '16', '17' ,'18' ,'19' ,'20' ,'21' ,'22' ,'23', '24' ,'25' ,'26' ,'27', '28' ,'29', '30' ,'31']
    months = ['01', '02' ,'03', '04', '05' ,'06', '07', '08', '09', '10', '11', '12']
    years = ['2005', '2006', '2007', '2008', '2009', '2010']
    sessions = ['200405', '200506' ,'200607', '200708', '200809' ,'200910']

    for session in sessions:
        for year in years:
            for month in months:
                for day in days:

                    date = year[2:4]+month+day
                    if year[2] == '0':
                        dateShort = year[3:4]+month+day
                    else:
                        dateShort = date
                    # print "Trying session: ",session, " Date: ", date
                    contentsURL1 = "https://publications.parliament.uk/pa/cm"+session+"/cmhansrd/cm"+date+"/debindx/"+dateShort+"-x.htm"
                    contentsURL2 = "https://publications.parliament.uk/pa/cm"+session+"/cmhansrd/vo"+date+"/debindx/"+dateShort+"-x.htm"

                    contentsPage1 = urllib2.urlopen(contentsURL1).read()
                    contentsPage2 = urllib2.urlopen(contentsURL2).read()

                    contentsSoup1 = BeautifulSoup(contentsPage1,'lxml')
                    contentsSoup2 = BeautifulSoup(contentsPage2,'lxml')

                    if contentsSoup1.find("h1"):

                    response1 = contentsSoup1.find("h1").getText().strip()
                    response2 = contentsSoup2.find("h1").getText().strip()

                    if response1 != "Page cannot be found":
                        print "Correct CM URL: ",contentsURL1
                    elif response2 != "Page cannot be found":
                        print "Correct VO URL: ",contentsURL2

                    # if contentsSoup.find("h1").getText().strip() != "Page cannot be found":
                    #     print "Page exists"
                    #     print "URL is: ", contentsURL
                    #     # contentsResults = contentsSoup.find_all("p", {"style": "text-align:center;text-transform:capitalize;margin:0 !important;padding:2px;"})
                    #     # searchURL = contentsResults.find_all('a', href=True)['href']
                    #     # searchPage = urllib2.urlopen(searchURL).read()
                    #     # searchSoup = BeautifulSoup(searchPage,'lxml')
                    #     #
                    #     # searchResults = searchSoup.body.find_all(string=re.compile('.*{0}.*'.format(searchTerm)), recursive=True)
                    #     # if len(searchResults) > 0:
                    #     #     for result in searchResults:
                    #     #         contribDateFormat = datetime.strptime(" ".join([day, month, year]), '%d %m %Y')
                    #     #         contributionDates.append(contribDateFormat)
                    # else:
                    #     print "Page doesn't exist"
                    #     print "URL is: ", contentsURL
                    #     print "..."

    return contributionDates

def getNewContribs(searchTerm):

    contributionDates = []

    # search new records from 2006-present day

    pageNum=1

    initURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(pageNum)+"&house=Commons"
    initPage = urllib2.urlopen(initURL).read()
    initSoup = BeautifulSoup(initPage,'lxml')

    if initSoup.find("p", {"class": "pagination-total"}):

        totalPages = int(initSoup.find("p", {"class": "pagination-total"}).getText().replace(',','').replace('(','').replace(')','').split()[-1])

        for i in range(1,totalPages+1):

            print "Parsing new page ", i, " of ", totalPages

            searchURL = "http://hansard.parliament.uk/search/Contributions?searchTerm="+searchTerm+"&page="+str(i)+"&house=Commons"
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

    uniqueDates = sorted(set(contributionDates))
    uniqueCounts = []

    print (contributionDates)

    for date in uniqueDates:
        uniqueCounts.append(contributionDates.count(date))

    matplotlib.rcParams['toolbar'] = 'None' # switch off toolbar
    plt.bar(uniqueDates,uniqueCounts,color='b',width=5)
    plt.title(searchTerm)
    plt.gcf().autofmt_xdate()
    plt.show()

    return uniqueDates, uniqueCounts

searchTerm = "internet"
# contributionDatesOld = getOldContribs(searchTerm)
contributionDatesMid = getMidContribs(searchTerm)
# contributionDatesNew = getNewContribs(searchTerm)
# [uniqueDates, uniqueCounts] = plotContribs(searchTerm,contributionDatesNew)

