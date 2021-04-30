from selenium import webdriver
import os

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())
driver.implicitly_wait(10.0)
baseurl = 'https://sra.org.uk/consumers/register/'
driver.get(baseurl)
filename = "lawyer-directory.csv"
firmCount = {
    "Law": 2424,
    "Legal": 1245,
    "Solicitor": 4728,
    "Lawyer": 202,
    "Ltd": 2749,
    "Limited": 8311,
    "LLP": 2449
}

initialResults = 5

try:
    sraCookieBannerAccept = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div/div/div/button')
    sraCookieBannerAccept.click()

    firmTab = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[3]/div[1]/ul/li[3]/a')
    firmTab.click()

    searchBox = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[2]/form/div[1]/input[1]')
    searchBox.click()
    searchBox.send_keys('Law')

    searchButton = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[2]/form/div[1]/div/button/i')
    searchButton.click()

    # Total Firms by Search Term
    searchResults = driver.find_element_by_id('allSearchResults')

    showMoreLink = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[4]/div[1]/div[1]/div/a')

    totalNumberOfFirmsElement = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[4]/div[1]/div[1]/div')
    totalFirms = int(totalNumberOfFirmsElement.text[22:26]) + initialResults

    # timesToClickShowMore = round(totalFirms / 5) - 1

    for i in range(0, totalFirms):
        if i > 0 and i % 5 == 0:
            print(str(i))
            showMoreLink.click()
        else:
            print("first 5")
    print("test")

except NoSuchElementException:
    driver.close()
