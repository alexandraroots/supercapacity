import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import requests
from urllib.request import Request, urlopen
from selenium import webdriver
import time


if __name__ == "__main__":
    driver = webdriver.Safari()
    url = 'https://app.dimensions.ai/discover/publication?search_mode=content&search_text=NiCo2O4%20hydrothermal%20supercapacitor&search_type=kws&search_field=full_search'
    driver.set_window_size(1400, 1000)
    driver.get(url)
    SCROLL_PAUSE_TIME = 2

    time.sleep(SCROLL_PAUSE_TIME)

    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")

    comment_items = soup.find_all('div', {'class': "sc-18gkrbr-0 hvtxgn"})
    print(comment_items)

    # get_element = driver.find_elements_by_css_selector("#mainContentBlock > div.sc-cOLXoO.fHwisV > div > div.sc-mcj13m-0.dWCyOa > div:nth-child(3) > div.mathjax.resultList.resultList--publications > div:nth-child(3)")
    # print(len(get_element))
    # html_page = urlopen(url).read()
    # soup = BeautifulSoup(html_page, 'html.parser')
    # print(soup)
    # print(soup.select('//*[@id="mainContentBlock"]/div[3]/div/div[2]/div[2]/div[1]/div[2]'))
    # response = requests.get(url)
    # print(response[])
    # html_element = html.fromstring(response.text)
    # top_tags = html_element.xpath('//*[@id="mainContentBlock"]/div[3]/div/div[2]/div[2]/div[1]/div[2]')
    # print(top_tags)
    # # i_need_element = soup.select('*[@id*="mainContentBlock"]/div[3]/div/div[2]/div[2]/div[1]/div[2]')
    # # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'lxml')
    # # quotes = soup.find_all('#mainContentBlock > div.sc-cOLXoO.fHwisV > div > div.sc-mcj13m-0.dWCyOa > div:nth-child(3) > div.mathjax.resultList.resultList--publications > div:nth-child(2)', class_='text')
    # for link in soup.select('thjax.resultList.resultList--publications > div:nth-child(2)'):
    #     print(link)
    # print(soup.find_all('//*[@id="mainContentBlock"]/div[3]/div/div[2]/div[2]/div[1]/div[2]'))

    #'//*[@id="mainContentBlock"]/div[3]/div/div[2]/div[2]/div[1]/div[2]'
    # print(quotes)



