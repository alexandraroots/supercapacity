from bs4 import BeautifulSoup
from selenium import webdriver
import time
from scroll import scroll
from url_from_doi import get_paper_url_from_doi
import logging

PAUSE_TIME = 2.0

if __name__ == "__main__":
    driver = webdriver.Safari()
    url = "https://app.dimensions.ai/discover/publication?search_mode=content&search_text=NiCo2O4%20hydrothermal%20supercapacitor&search_type=kws&search_field=full_search"
    driver.set_window_size(1400, 1000)
    driver.get(url)
    SCROLL_PAUSE_TIME = 2

    time.sleep(PAUSE_TIME)

    scroll(driver, 5)
    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")

    comment_items = soup.find_all("span", {"class": "__readcube-access-button"})
    doi = []
    urls = []
    for elem in comment_items:
        curr_doi = elem['data-doi']
        doi.append(curr_doi)
        try:
            full_url = get_paper_url_from_doi(curr_doi)
            urls.append(full_url)
        except:
            logging.warning(f'{curr_doi}')

    print(urls)
    print(len(urls))
    print(len(comment_items))



