# import libraries
import urllib2
from bs4 import BeautifulSoup
import math
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import re
import os
import time
from glob import glob
import calendar
from collections import Counter
import string
import pickle

def searchContribs(searchTerms,startDate,endDate):

    uniqueDates = []
    uniqueCounts = []

    start = datetime.strptime(startDate, '%d %m %Y')
    end = datetime.strptime(endDate, '%d %m %Y')


    for dictFilePath in glob("./Dicts/*.p"):

        contribDate = datetime.strptime(" ".join([dictFilePath.split("/")[2].split(" ")[2][0:2], dictFilePath.split("/")[2].split(" ")[1].zfill(2), dictFilePath.split("/")[2].split(" ")[0]]), '%d %m %Y')

        if contribDate >= start and contribDate <= end:
            clear_output(wait=True)
            print "opening: ", dictFilePath
            wordDict = pickle.load( open( dictFilePath, "rb" ) )
            counts = 0
            wordFlag=0
            for term1 in searchTerms:
                if wordDict[term1]:
                    wordFlag = 1

            if wordFlag:
                uniqueDates.append(contribDate)
                for term2 in searchTerms:
                    counts = counts + wordDict[term2]
                uniqueCounts.append(counts)

    return uniqueDates, uniqueCounts
