from lxml import html
import requests
import argparse
import sys
import os
import re
from requests.auth import HTTPBasicAuth
# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#install phontomjs https://gist.github.com/julionc/7476620

def getBoardsResultList(url):

    sys.stdout.write('Validating URL\n')

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    isValid = re.match(regex, url) is not None  # True
    if (isValid==False):
        sys.stdout.write('URL is not valid\n')
        return -1
    sys.stdout.write('URL validation succedded\n')

    #driver = webdriver.Firefox()  # if you want to use chrome, replace Firefox() with Chrome()
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--enable-javascript")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
    # driver = webdriver.Chrome(chrome_options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    driver.get(url)  # load the web page
    WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "listing")))  # waits till the element with the specific id appears
    page = driver.page_source  # gets the html source of the page

    tree = html.fromstring(page)
    urls = tree.xpath('//a/@href')
    newUrlDict = {}
    for url in urls:
        if('http' not in url):
            continue;
        url = url[:-1]
        newUrlDict[url.rsplit('/', 1)[-1]]=url

    sys.stdout.write('\n\nList of boards and links to scrap:\n')
    for board in newUrlDict:
        print board + ' : ' + newUrlDict.get(board, "none")


def main():
    
    sys.stdout.write('Scrapping Tool For ARM Jenkins Test Result\n')
    url = 'http://mbed-os-logs.s3-website-us-west-1.amazonaws.com/?prefix=logs/7383/2272/PASS/'
    sys.stdout.write('Contacting URL: ' + url + '\n')
    getBoardsResultList(url)

main()
sys.stdout.write('-------------------- ALL DONE --------------------\n')
sys.stdout.flush()
