from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

import argparse
import class_dicts
import re
import datetime as dt
import pytz

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='Email login.')
    parser.add_argument('password', help='Password login.')
    parser.add_argument('class_key', help='Dictionary key for the class, must be exact.')
    parser.add_argument('--book_at_noon', type=bool, default=False, help='Only start trying to book at 12pm noon.')
    # parser.add_argument('--start_time', default=None,
    #                     help='Start time of the class; if not present, choose first class.')
    args = parser.parse_args()

    email = args.email
    password = args.password
    class_key = args.class_key
    book_at_noon = args.book_at_noon

    browser = webdriver.Chrome()

    browser.get('https://portal.fitlerclub.com/group-fitness/calendar')
    sleep(2.1)

    while book_at_noon:
        edt_tz = pytz.timezone('US/Eastern')
        if (dt.datetime.now(tz=edt_tz).hour < 11 or dt.datetime.now(tz=edt_tz).minute < 59 or \
            dt.datetime.now(tz=edt_tz).second < 57) or \
                (dt.datetime.now(tz=edt_tz).hour > 12 or dt.datetime.now(tz=edt_tz).minute > 3):
            sleep(0.2)
            continue
        else:
            book_at_noon = False

    email_input = browser.find_element(By.ID, 'email')
    email_input.send_keys(email)
    password_input = browser.find_element(By.ID, 'password')
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # get class dict to work on
    class_dict = class_dicts.classes[class_key]

    successful_reserve = False
    while not successful_reserve:
        sleep(1)

        next_button = browser.find_element(By.XPATH,
                                           "/html/body/div[1]/main/div[3]/div[1]/div/div[1]/div[3]/div/button[2]")
        next_button.click()

        calendar_table = browser.find_element(By.XPATH,
                                              '/html/body/div[1]/main/div[3]/div[1]/div/div[2]/div/table/tbody/tr/td/div/div/div/div[2]/table')

        for row in calendar_table.find_elements(By.CSS_SELECTOR, 'tr'):
            if successful_reserve:
                continue

            for cell in row.find_elements(By.TAG_NAME, 'td'):
                try:
                    time, name, is_open = cell.text.split('\n')
                    start_time = time.split(' - ')[0]
                    print(start_time, name, is_open)

                    if is_open.lower() == 'reservations open' and name.lower() == class_dict.get(
                            'class_name') and start_time.lower() == class_dict.get('start_time'):
                        cell.click()
                        sleep(1)

                        date_field = browser.find_element(By.XPATH,
                                                          '/html/body/div[6]/div[2]/div[4]/div/div/div/div[1]/p[1]')
                        weekday = re.findall(r'DATE: (\w+)', date_field.text)

                        if len(weekday) == 0:
                            continue
                        if weekday[0].lower() != class_dict.get('weekday'):
                            continue

                        # reserve_button = browser.find_element(By.XPATH, '//*[@id="event-details"]/div/div[3]/form/button')
                        reserve_button = browser.find_element(By.XPATH,
                                                              '/html/body/div[6]/div[2]/div[4]/div/div/div/div[3]/form/button')
                        reserve_button.click()
                        sleep(1)

                        try:
                            is_success_element = browser.find_element(By.XPATH, '/html/body/div[1]/header/div[2]')
                            if re.search('successfully', is_success_element.text.lower()):
                                successful_reserve = True
                                break
                        except:
                            pass

                except ValueError:
                    pass

        if not successful_reserve:
            sleep(1)
            browser.refresh()

    print(f'Successfully reserved class {class_key}')
