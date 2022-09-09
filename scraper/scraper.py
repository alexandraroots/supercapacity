from bs4 import BeautifulSoup
from selenium import webdriver
import time
from scroll import scroll
from url_from_doi import get_paper_url_from_doi
import logging
from helpers import save_to_csv

PAUSE_TIME = 2.0

if __name__ == "__main__":
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)

    driver = webdriver.Safari()
    url = "https://app.dimensions.ai/discover/publication?search_mode=content&search_text=NiCo2O4%20hydrothermal%20supercapacitor&search_type=kws&search_field=full_search"
    driver.set_window_size(1400, 1000)
    driver.get(url)
    SCROLL_PAUSE_TIME = 2

    time.sleep(PAUSE_TIME)
    try:
        scroll(driver, 100, logger)
    except:
        logger.warning('End of scrolling')
    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("span", {"class": "__readcube-access-button"})
    names = soup.find_all("a", {"class": "sc-w3owpf-0 kcWhXH sc-w3owpf-1 sc-z0mrsy-0 bjirTh ievwkh sc-pVTFL cIWYDt"})
    descriptions = soup.find_all("div", {"class" : "sc-llYSUQ bwRYzw sc-5tt51r-0 qvZbr"})
    doi = []
    urls = []
    result = []
    n = len(items)
    try:
        for i, (name, elem) in enumerate(zip(names, items)):
            name_text = name.find('span').text
            logger.info(f'{i} elem / {n}')
            full_elem = {}
            curr_doi = elem['data-doi']
            full_elem['doi'] = curr_doi
            full_elem['name'] = name_text
            full_elem['description'] = descriptions[i].find('span').text
            doi.append(curr_doi)
            # try:
            #     full_url = get_paper_url_from_doi(curr_doi)
            #     urls.append(full_url)
            #     full_elem['url'] = full_url
            # except:
            #     logger.warning(f'{curr_doi}')
            #     full_elem['url'] = None

            result.append(full_elem)
    except:
        save_to_csv(result)

    save_to_csv(result)



