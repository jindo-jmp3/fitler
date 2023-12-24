from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

import argparse
import class_dicts
import re


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='Email login.')
    parser.add_argument('password', help='Password login.')
    # parser.add_argument('class_name', help='Name of the class, must be exact.')
    # parser.add_argument('day_of_week', help='Day of the week for the class.')
    # parser.add_argument('--start_time', default=None,
    #                     help='Start time of the class; if not present, choose first class.')
    args = parser.parse_args()

    email = args.email
    password = args.password

    browser = webdriver.Chrome()

    browser.get('https://portal.fitlerclub.com/group-fitness/calendar')
    sleep(2.1)

    email_input = browser.find_element(By.ID, 'email')
    email_input.send_keys(email)
    password_input = browser.find_element(By.ID, 'password')
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    next_button = browser.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div[1]/div/div[1]/div[3]/div/button[2]")
    sleep(0.6)
    next_button.click()

    # get class dict to work on
    class_dict = class_dicts.classes['wednesday_power_flow']

    calendar_table = browser.find_element(By.XPATH,
                                          '/html/body/div[1]/main/div[3]/div[1]/div/div[2]/div/table/tbody/tr/td/div/div/div/div[2]/table')
    for row in calendar_table.find_elements(By.CSS_SELECTOR, 'tr'):
        for cell in row.find_elements(By.TAG_NAME, 'td'):
            try:
                time, name, is_open = cell.text.split('\n')
                start_time = time.split(' - ')[0]

                if is_open.lower() == 'reservations open' and name.lower() == class_dict.get(
                        'class_name') and start_time.lower() == class_dict.get('start_time'):
                    cell.click()

                    date = browser.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[4]/div/div/div/div[1]/p[1]')
                    weekday = re.findall(r'DATE: (\w+)', date.text)

                    if len(weekday) == 0:
                        continue
                    if weekday[0].lower() != class_dict.get('weekday'):
                        continue

                    # reserve_button = browser.find_element(By.XPATH, '//*[@id="event-details"]/div/div[3]/form/button')
                    reserve_button = browser.find_element(By.XPATH,
                                                          '/html/body/div[6]/div[2]/div[4]/div/div/div/div[3]/form/button')
                    reserve_button.click()
            except ValueError:
                pass

    print()
