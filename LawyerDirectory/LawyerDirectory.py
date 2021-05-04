from selenium import webdriver
import os
from sys import platform

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())
driver.implicitly_wait(10.0)
baseurl = 'https://sra.org.uk/consumers/register/'
driver.get(baseurl)
filename = "lawyer-directory.csv"


def close_window():
    if platform == "darwin":
        driver.switch_to.window(driver.window_handles[1])
        driver.close()


def open_firm_in_new_tab(firm_link):
    driver.execute_script("window.open( \"" + firm_link + "\", '_blank')")


initialResults = 5

try:
    sraCookieBannerAccept = driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div/div/div/button')
    sraCookieBannerAccept.click()

    firmTab = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[3]/div[1]/ul/li[3]/a')
    firmTab.click()

    searchBox = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[2]/form/div[1]/input[1]')
    searchBox.click()
    searchBox.send_keys('Law')

    searchButton = driver.find_element_by_xpath(
        '/html/body/div[1]/section/div/article/div/div[2]/form/div[1]/div/button/i')
    searchButton.click()

    # Total Firms by Search Term
    searchResults = driver.find_element_by_id('allSearchResults')

    showMoreLink = driver.find_element_by_xpath('/html/body/div[1]/section/div/article/div/div[4]/div[1]/div[1]/div/a')

    totalNumberOfFirmsElement = driver.find_element_by_xpath(
        '/html/body/div[1]/section/div/article/div/div[4]/div[1]/div[1]/div')
    totalFirms = int(totalNumberOfFirmsElement.text[22:26])
    # timesToClickShowMore = round(totalFirms / 5) - 1

    for i in range(1, totalFirms + 1):
        firmRow = driver.find_element_by_id('firm-row-id-' + str(i))
        firmLink = firmRow.find_element_by_xpath(
            "/html/body/div[1]/section/div/article/div/div[4]/div[1]/article/ul/li["+str(i)+"]/a").get_attribute("href")

        open_firm_in_new_tab(firmLink)

        # loads 50 at a time, but after the first 5 are processed
        if i % 5 == 0:
            showMoreLink.click()



    print("test")

except NoSuchElementException:
    driver.close()
