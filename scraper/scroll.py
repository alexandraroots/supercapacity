import time
import logging

SCROLL_PAUSE_TIME = 3.0
PAGE_SIZE = 26000


def scroll(driver, count):
    i = 1
    while i < count:
        logging.warning(f"Page {i} downloaded")
        i += 1
        time.sleep(SCROLL_PAUSE_TIME)
        last_pixel = i * PAGE_SIZE
        driver.execute_script(f"window.scrollTo(0, {last_pixel})")
