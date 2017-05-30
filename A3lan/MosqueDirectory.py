import bs4
import io
from urllib import urlopen as uReq
from bs4 import BeautifulSoup as soup

baseurl = 'http://www.mosquedirectory.co.uk';
mosques = '/browse-mosques/alphabet/letter/A/1'

lettersArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def parseMosqueInfo(mosque_info_html):
    print ("woo")



def parseUrl(symbolicUrl):
    cleanedUrl = str(symbolicUrl)
    cleanedUrl = cleanedUrl.replace("<a href=\"../../../../../mosques", "")
    splitComponents = cleanedUrl.split("\">")

    newUrl = baseurl+"/mosques"+splitComponents[0]

    return newUrl

def parseMosqueList(mosque_list_url):

    # Opening connection
    uClient = uReq(mosque_list_url)

    # Grabs the HTML
    page_html = uClient.read()

    # HTML Parsing
    page_soup = soup(page_html, "html.parser")

    uClient.close()

    mosqueSearchTag = page_soup.findAll("ul", {"id": "mosque_list"})

    listOfMosques = mosqueSearchTag[0].findAll("li")

    for mosque in listOfMosques:
        mosqueUrl = parseUrl(mosque.find("a"))

        # open connection to mosque page
        uClient = uReq(mosqueUrl)
        mosqueDetail_html = uClient.read()
        uClient.close()
        # TODO Manipulate HTML to get requried data
        parseMosqueInfo(mosqueDetail_html)

for letter in lettersArray:

    # # Always start at page one and increment if there are more pages for a letter
    pageNumber = 1

    pageUrl = baseurl+"/browse-mosques/alphabet/letter/"+letter+"/"+str(pageNumber)

    # Opening connection
    uClient = uReq(pageUrl)

    # Grabs the HTML
    page_html = uClient.read()

    # HTML Parsing
    page_soup = soup(page_html, "html.parser")

    uClient.close()

    try:
        totalPages = int(page_soup.find("a", {}, True, "[Last Page]").attrs['href'])
    except:
        print("couldnt get it")

    i = totalPages
    while pageNumber <= totalPages:
            newPageUrl = baseurl + "/browse-mosques/alphabet/letter/" + letter + "/" + str(pageNumber)
            parseMosqueList(newPageUrl)
            pageNumber = pageNumber + 1


print(page_soup)

