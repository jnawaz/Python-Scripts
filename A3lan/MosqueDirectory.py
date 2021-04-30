import bs4
import io
from urllib import urlopen as uReq
from bs4 import BeautifulSoup as soup

baseurl = 'http://www.mosquedirectory.co.uk';
mosques = '/browse-mosques/alphabet/letter/A/1'

filename = "mosque.csv"
f = open(filename, "w")

isZedAndLastPage = False

lettersArray = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def create_file():
    headers = "mosque name, address, postcode, telephone, fax, capacity\n"
    f.write(headers)

def parse_mosque_name(mosque_url):
    components = str(mosque_url).split("\">")
    return components[1].split("(")[0].strip()

def parseMosqueInfo(mosque_info_html, mosque_name):
    mosque_info_contents = mosque_info_html.find("div", {"id":"mosque_info_contents"})

    tds = mosque_info_contents.findAll("td")

    for td in tds:
        try:
            rows = td.findAll("td")
            if len(rows) > 0:
                # Get Address
                if tds[3].find("span", {"class":"style3"}, True, "Address : ") :
                    address = tds[4].contents[0]

                if tds[5].find("span", {"class":"style3"}, True, "Postcode :") :
                    postcode = tds[6].contents[0]

                if tds[9].find("span", {"class":"style3"}, True, "Telephone :") :
                    telephone = tds[10].contents[0]

                if tds[11].find("span", {"class":"style3"}, True, "Fax :") :
                    fax = tds[12].contents[0]

                if tds[13].find("span", {"class":"style3"}, True, "Capacity : ") :
                    capacity = tds[14].contents[0]

                f.write(mosque_name + "," + address + "," + postcode + "," + telephone + "," + fax + "," + capacity + "\n")

                if isZedAndLastPage:
                    f.close()

        except:
            print "not found"

def parseUrl(symbolicUrl):
    cleanedUrl = str(symbolicUrl)
    cleanedUrl = cleanedUrl.replace("<a href=\"../../../../../mosques", "")
    cleanedUrl = cleanedUrl.replace(".-", "-")
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
        mosque_name = parse_mosque_name(mosque)
        # open connection to mosque page
        uClient = uReq(mosqueUrl)
        print mosqueUrl
        mosqueDetail_html = uClient.read()
        soup_mosque_detail = soup(mosqueDetail_html, "html.parser")
        uClient.close()
        # TODO Manipulate HTML to get requried data
        try:
            parseMosqueInfo(soup_mosque_detail, mosque_name)
        except:
            print ("error with mosque html minor, move on")

#create csv - Program Start
create_file()
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
            if letter == "Z" and pageNumber == totalPages:
                isZedAndLastPage = True

            newPageUrl = baseurl + "/browse-mosques/alphabet/letter/" + letter + "/" + str(pageNumber)
            parseMosqueList(newPageUrl)
            pageNumber = pageNumber + 1

