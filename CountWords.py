# import libraries
from bs4 import BeautifulSoup
import glob
import collections
from nltk import ngrams
import codecs


# combine member contributions from a given volume into one txt file
def getContributions(volName):

    contributionsFile= open(volName+"_contributions.txt","w+")

    for xmlFileName in glob.glob("./"+volName+"/*.xml"): # for every XML file in the folder, read and concatenate its contents
        xmlFile = open(xmlFileName,"r")
        xmlContents = xmlFile.read()
        soup = BeautifulSoup(xmlContents,'xml') # parse the contents using beautiful soup
        memberContributions = soup.find_all('membercontribution') # find all member contribution tags

        for contribution in memberContributions: # write member contributions to text file
            cleanContrib = contribution.get_text().encode('utf-8').strip()
            contributionsFile.write(cleanContrib)

        xmlFile.close()

    contributionsFile.close()
    print("all done!")

# extract n-grams from member contributions and print the 'p' most frequently occurring phrases
def getFreqs(volName,n,p):

    contributionsFile= codecs.open(volName+"_contributions.txt","r","utf-8")
    words = contributionsFile.read()
    nGrams = ngrams(words.split(), n)
    phraseList = []
    for phrase in nGrams:

        phraseList.append(' '.join(phrase).replace(',', '').replace('.', '').replace('"', '').replace('?', '').replace('!', '').replace(';', '').replace(':', '').lower())

    print "List constructed! Length: ", len(phraseList)
    counter=collections.Counter(phraseList)
    print counter.most_common(p)

getContributions("1909")
getFreqs("1909",1,500)