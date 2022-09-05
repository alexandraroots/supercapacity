from selenium import webdriver
import time
import logging

if __name__ == "__main__":
    driver = webdriver.Safari()
    url = 'https://app.dimensions.ai/discover/publication?search_mode=content&search_text=NiCo2O4%20hydrothermal%20supercapacitor&search_type=kws&search_field=full_search'
    driver.set_window_size(1400, 1000)
    driver.get(url)


    SCROLL_PAUSE_TIME = 1.0

    i = 1
    while True:
        logging.warning(f'Page {i}')
        i += 1
        time.sleep(SCROLL_PAUSE_TIME)
        last_pixel = i * 26000
        driver.execute_script(f"window.scrollTo(0, {last_pixel})")
