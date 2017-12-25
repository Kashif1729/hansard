# import libraries
import urllib2
from bs4 import BeautifulSoup
import math
from datetime import datetime
import matplotlib.pyplot as plt
import re
import os
import time
from glob import glob
import calendar

# function to save daily Hansard records from 2005-2010 locally as HTML files
def saveMidContribs():

    days = ['01', '02', '03', '04', '05', '06', '07' ,'08' ,'09', '10', '11' ,'12', '13', '14' ,'15',
            '16', '17' ,'18' ,'19' ,'20' ,'21' ,'22' ,'23', '24' ,'25' ,'26' ,'27', '28' ,'29', '30' ,'31']

    validSessions = ['200405 2004 11','200405 2004 12', '200405 2005 01', '200405 2005 02','200405 2005 03','200405 2005 04',
                     '200506 2005 05','200506 2005 06','200506 2005 07','200506 2005 08','200506 2005 09','200506 2005 10',
                     '200506 2005 11','200506 2005 12',
                     '200506 2006 01','200506 2006 02','200506 2006 03','200506 2006 04','200506 2006 05','200506 2006 06',
                     '200506 2006 07','200506 2006 08','200506 2006 09','200506 2006 10','200506 2006 11',
                     '200607 2006 12','200607 2007 01','200607 2007 02','200607 2007 03','200607 2007 04','200607 2007 05','200607 2007 06',
                     '200607 2007 07','200607 2007 08','200607 2007 09','200607 2007 10',
                     '200708 2007 11','200708 2007 12',
                     '200708 2008 01','200708 2008 02','200708 2008 03','200708 2008 04','200708 2008 05','200708 2008 06',
                     '200708 2008 07','200708 2008 08','200708 2008 09','200708 2008 10','200708 2008 11',
                     '200809 2008 12',
                     '200809 2009 01','200809 2009 02','200809 2009 03','200809 2009 04','200809 2009 05','200809 2009 06',
                     '200809 2009 07','200809 2009 08','200809 2009 09','200809 2009 10','200809 2009 11',
                     '200910 2009 12',
                     '200910 2010 01','200910 2010 02','200910 2010 03','200910 2010 04',
                     '201011 2010 05','201011 2010 06','201011 2010 07','201011 2010 08','201011 2010 09','201011 2010 10',
                     '201011 2010 11','201011 2010 12'
                     ]

    for sesh in validSessions:
        for day in days:

            session, year, month = sesh.split(" ")

            date = year[2:4]+month+day

            print "trying date ",date

            try:
                currentDate = time.strptime(day+'/'+month+'/'+year,'%d/%m/%Y')

                if year[2] == '0':
                    dateShort = year[3:4]+month+day
                else:
                    dateShort = date

                if time.strptime('04/05/2006','%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year,'%d/%m/%Y'):
                    pageFlag = "-0001.htm"
                else:
                    pageFlag = "-01.htm"

                if  time.strptime('08/11/2006','%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year,'%d/%m/%Y'):
                    volFlag = "cm"
                else:
                    volFlag = "vo"

                contentsURL = "https://publications.parliament.uk/pa/cm"+session+"/cmhansrd/"+volFlag+date+"/debtext/"+dateShort+pageFlag
                contentsPage = urllib2.urlopen(contentsURL).read()
                contentsSoup = BeautifulSoup(contentsPage,'lxml')

                if contentsSoup.find("h1") is None:
                    print "success!"
                    print "..."
                    saveFile = open('./'+session+' '+year+' '+month+' '+day+'.html', 'w')
                    for pageNum in range(1,2000):
                        print "trying page ",pageNum
                        if time.strptime('04/05/2006','%d/%m/%Y') < time.strptime(day+'/'+month+'/'+year,'%d/%m/%Y'):
                            pageFlag = '-'+str(pageNum).zfill(4)+'.htm'
                        else:
                            pageFlag = '-'+str(pageNum).zfill(2)+'.htm'

                        searchURL = "https://publications.parliament.uk/pa/cm"+session+"/cmhansrd/"+volFlag+date+"/debtext/"+dateShort+pageFlag
                        searchPage = urllib2.urlopen(searchURL).read()
                        searchSoup = BeautifulSoup(searchPage,'lxml')
                        if searchSoup.find("h1") is None:
                            saveFile.write(searchPage)
                        else:
                            break
                    saveFile.close()
                else:
                    print "no debates on this day!"

            except:
                print "not a valid date!"

# function to save daily Hansard records from 1803-2004 locally as HTML files
def saveOldContribs():

    for year in range(1924,2005): #2005):
        for month in range(1,13):
            for day in range(1,32):

                monthName = calendar.month_name[month].lower()[0:3]
                contentsURL = "http://hansard.millbanksystems.com/sittings/"+str(year)+"/"+monthName+"/"+str(day).zfill(2)

                try:
                    print "trying date: ", str(year)+' '+str(month)+' '+str(day).zfill(2)
                    contentsPage = urllib2.urlopen(contentsURL).read()
                    contentsSoup = BeautifulSoup(contentsPage,'lxml')
                    print "success!"
                    saveFile = open('./XXXX'+ ' '+str(year)+' '+str(month)+' '+str(day).zfill(2)+'.html', 'w')
                    commonsSection = contentsSoup.find_all("ol", {"class": "xoxo first"})[0]
                    for link in commonsSection.find_all('a', href=True):
                        linkURL = "http://hansard.millbanksystems.com"+link['href']
                        print linkURL
                        linkPage = urllib2.urlopen(linkURL).read()
                        saveFile.write(linkPage)

                    saveFile.close()
                except:
                    print "page not found!"

def saveNewContribs():

    for year in range(2011,2018):
        for month in range(1,13):
            for day in range(1,32):

                contentsURL = "http://hansard.parliament.uk/commons/"+str(year)+"-"+str(month).zfill(2)+"-"+str(day).zfill(2)

                print "trying date: ", str(year)+' '+str(month)+' '+str(day).zfill(2)
                print contentsURL
                contentsPage = urllib2.urlopen(contentsURL).read()
                contentsSoup = BeautifulSoup(contentsPage,'lxml')
                commonsSection = contentsSoup.find_all("li", {"class": "no-children"})
                if commonsSection:
                    print "success!"
                    saveFile = open('./XXXX'+ ' '+str(year)+' '+str(month)+' '+str(day).zfill(2)+'.html', 'w')
                    for listItem in commonsSection:
                        linkURL = "http://hansard.parliament.uk"+listItem.find('a', href=True)['href']
                        print linkURL
                        linkPage = urllib2.urlopen(linkURL).read()
                        linkSoup = BeautifulSoup(linkPage,'lxml')
                        saveFile.write(linkPage)
                else:
                    print "no sittings"

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

def getMidContribs(searchTerm,contributionDates): # this is super gross

    directories = os.listdir("./")

    for htmlFilePath in glob("./*/*.html"):
        # print htmlFilePath

        year = htmlFilePath.split("/")[1].split(" ")[1]
        month = htmlFilePath.split("/")[1].split(" ")[2]
        day = htmlFilePath.split("/")[2].split(" ")[0][0:2]

        print year, month, day

        htmlFile = open(htmlFilePath,'r')
        fileSoup = BeautifulSoup(htmlFile.read(),'lxml')
        searchResults = fileSoup.body.find_all(string=re.compile('.*{0}.*'.format(searchTerm)), recursive=True)
        if len(searchResults) > 0:
            for result in searchResults:
                contribDateFormat = datetime.strptime(" ".join([day, month, year]), '%d %m %Y')
                contributionDates.append(contribDateFormat)
        htmlFile.close()

    return contributionDates

def getNewContribs(searchTerm,contributionDates):

    # contributionDates = []

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

def searchContribs(searchTerm,startDate,endDate):

    contributionDates = []
    contributionCounts = []
    uniqueDates = []
    uniqueCounts = []

    for htmlFilePath in glob("./Archive/*.html"):

        year = htmlFilePath.split("/")[2].split(" ")[1]
        month = htmlFilePath.split("/")[2].split(" ")[2].zfill(2)
        day = htmlFilePath.split("/")[2].split(" ")[3][0:2]

        contribDate = datetime.strptime(" ".join([day, month, year]), '%d %m %Y')
        start = datetime.strptime(startDate, '%d %m %Y')
        end = datetime.strptime(endDate, '%d %m %Y')

        if contribDate >= start and contribDate <= end:
            print "opening: ", htmlFilePath
            htmlFile = open(htmlFilePath,'r')
            fileSoup = BeautifulSoup(htmlFile.read(),'html.parser')
            searchResults = fileSoup.find_all(string=re.compile('.*{0}.*'.format(searchTerm)),recursive=True)
            print searchResults
            if len(searchResults) > 0:
                for result in searchResults:
                    contributionDates.append(contribDate)

            htmlFile.close()

    uniqueDates = sorted(set(contributionDates))

    for date in uniqueDates:
        uniqueCounts.append(contributionDates.count(date))

    return uniqueDates, uniqueCounts

def plotContribs(searchTerm,contributionDates):

    uniqueDates = sorted(set(contributionDates))
    uniqueCounts = []

    print (contributionDates)

    for date in uniqueDates:
        uniqueCounts.append(contributionDates.count(date))

    # matplotlib.rcParams['toolbar'] = 'None' # switch off toolbar
    plt.bar(uniqueDates,uniqueCounts,color='b',width=5)
    plt.title(searchTerm)
    plt.gcf().autofmt_xdate()
    plt.show()

    return uniqueDates, uniqueCounts

searchTerm = "Europe"
startDate = '10 01 2011'
endDate = '12 01 2011'
dates, counts = searchContribs(searchTerm,startDate,endDate)
print dates, counts
#saveMidContribs()
#saveOldContribs()
#saveNewContribs()
# contributionDatesOld = getOldContribs(searchTerm)
# contributionDatesMid = getMidContribs(searchTerm,contributionDatesOld)
# contributionDatesNew = getNewContribs(searchTerm,contributionDatesMid)
# [uniqueDates, uniqueCounts] = plotContribs(searchTerm,contributionDatesNew)
