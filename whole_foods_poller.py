import bs4
import os
import sys
import time

from selenium import webdriver


TIME_SLOT_URL = 'https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1'
HTML_TAGS = {
    'div': 'ufss-date-select-toggle-text-availability',
    'h4': 'ufss-slotgroup-heading-text a-text-normal'
}
NO_DELIVERY_HTML_TAGS = {
    'h4': 'a-alert-heading'
}
OPEN_SLOT_TEXT = ['1-hour delivery windows', '2-hour delivery windows', 'Next available']
ALERT_PHRASE = 'MAKE ORDER NOW!'


class WholeFoodsPoller(object):
    def __init__(self, time_slot_url):
        self._chrome_driver = webdriver.Chrome()
        self._time_slot_url = time_slot_url

    def Run(self):
        print('Login, add items to your whole foods cart, then proceed to check out window.')
        self._chrome_driver.get(self._time_slot_url)

        while (self._chrome_driver.current_url != self._time_slot_url):
            print('Currently not at check out window, waiting...') 
            time.sleep(10)
        
        found_slots = False
        while not found_slots:
            print('Refreshing...')
            self._chrome_driver.refresh()
            html = self._chrome_driver.page_source
            soup_client = bs4.BeautifulSoup(html, "html.parser")
            time.sleep(5)

            # Look for common open slot text
            for tag in HTML_TAGS:
                if tag == 'div':
                    dates = soup_client.findAll(tag, {'class': HTML_TAGS[tag]})
                    for date in dates:
                        try:
                            if 'Not available' not in date.text:
                                print('Potential Slot Open 1!')
                                os.system('say %s' % ALERT_PHRASE)
                                found_slots = True
                                time.sleep(1500)
                        except AttributeError:
                            continue

                if tag == 'h4':
                    try:
                        tag_text = str([x.text for x in soup_client.findAll(tag, class_ = HTML_TAGS[tag])])
                    except AttributeError:
                        continue
                    if any(tag_text in text for text in OPEN_SLOT_TEXT):
                        print('Potential Slot Open 2!')
                        os.system('say %s' % ALERT_PHRASE)
                        found_slots = True
                        time.sleep(1500)

            # See if No Delivery text is missing, possible opening available
            for tag in NO_DELIVERY_HTML_TAGS:
                no_delivery_text = 'No delivery windows available. New windows are released throughout the day.'
                try:
                    tag_text = soup_client.find('h4', class_ = NO_DELIVERY_HTML_TAGS[tag]).text
                except AttributeError:
                    print('Potential Slot Open 3!')
                    os.system('say %s' % ALERT_PHRASE)
                    found_slots = True
                    time.sleep(1500)

                if no_delivery_text == tag_text:
                    print('No Delivery openings yet...')
                    continue


def main():
    whole_foods_poller = WholeFoodsPoller(TIME_SLOT_URL)
    whole_foods_poller.Run()

if __name__ == '__main__':
    main()