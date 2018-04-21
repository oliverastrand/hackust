import os
import os.path
import shutil
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import wikipedia
from bs4 import BeautifulSoup
import html


def is_int(s):
    """
    Check if a string is an integer
    :param s: the string to be checked
    :return: true if it is, false if it is not an int
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_restaurant_attractions(city_name, number_attr):
    """
    Get information about the best number_attr of restaurants in the city from Trip adviser
    :param city_name: The name of the city as a string where you want to look for restaurants
    :param number_attr: The number of restaurants you want to get
    :return: a dictionary with numbers from 1 to 15 as keys with relevant values (name of attr, location etc.)
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("download.default_directory=r'/home/svilen/NUS/Hackathon/HKUST_18'")

    chrome_path = executable_path = r'/home/svilen/NUS/SMNA/chromedriver'
    browser = webdriver.Chrome(chrome_path, chrome_options=options)
    browser.get("https://en.tripadvisor.com.hk/Restaurants")
    # go to city on trip adviser

    browser.find_element_by_xpath(
        '//*[@id="taplc_trip_search_home_restaurants_0"]/div[2]/div[1]/div/span/input').send_keys(city_name);
    # time.sleep(5)
    search_attempt = browser.find_element_by_id('SUBMIT_RESTAURANTS')
    search_attempt.click()
    try:
        myElem = WebDriverWait(browser, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="eatery_6963464"]/div[2]/div[1]/div[1]/a')))
    except TimeoutException:
        print("Loading took too much time!")

    # handle attractions
    # res_list = browser.find_elements_by_xpath('//*[@id="EATERY_SEARCH_RESULTS"]')
    # res_list = find_elements_by_css_selector("listing rebrand listingIndex-1 first")
    # listing rebrand listingIndex-1 first
    res_list = browser.find_elements_by_xpath("//div[@class='title']/a")
    links = []
    num_attr = 0
    for i in res_list:
        try:
            myElem = WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="eatery_6963464"]/div[2]/div[1]/div[1]/a')))
        except TimeoutException:
            print("Loading took too much time!")
        link = i.get_attribute("href")
        if num_attr <= number_attr:
            num_attr += 1
            links.append(link)

    all_restaurants = {}
    key = 1
    for i in links:
        browser.get(i)
        res_name = browser.find_elements_by_id('HEADING')[0].text
        address = browser.find_elements_by_class_name('street-address')[0].text
        rating = float(browser.find_elements_by_class_name('overallRating')[0].text)
        reviews = int(browser.find_elements_by_class_name('more')[0].text.split()[0].replace(',', ''))
        price_tag = browser.find_elements_by_xpath('//*[@id="taplc_location_detail_header_restaurants_0"]/div[2]/span[3]')[0].text
        if '-' in price_tag:
            price_tag = price_tag.split(' - ')
            # takes the average of the estimated prices
            # divided by 2 multiplied by 20 = multiplied by 10
            price_tag = (price_tag[0].count('$') + price_tag[1].count('$'))*10
        else:
            price_tag = price_tag.count('$')*20
        # static estimated eating time of 60 minutes
        duration = 60
        all_restaurants[key] = {}
        all_restaurants[key]['name'] = res_name
        all_restaurants[key]['city'] = city_name
        all_restaurants[key]["address"] = address
        all_restaurants[key]["rating"] = rating
        all_restaurants[key]["reviews"] = reviews
        all_restaurants[key]["duration"] = duration
        all_restaurants[key]["price"] = price_tag
        key += 1
        time.sleep(2)
        browser.back()

    with open(city_name + "_restaurants.json", 'w') as out:
        json.dump(all_restaurants, out)

    return all_restaurants



def get_city_attractions(city_name, number_attr):
    """
    Get information about the best number_attr of city attractions from Trip adviser
    :param city_name: The name of the city as a string which you want to get all attractions for
    :param number_attr: The number of attractions you want to get
    :return: a dictionary with numbers from 1 to 15 as keys with relevant values (name of attr, location etc.)
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("download.default_directory=r'/home/svilen/NUS/Hackathon/HKUST_18'")

    chrome_path = executable_path=r'/home/svilen/NUS/SMNA/chromedriver'
    browser = webdriver.Chrome(chrome_path, chrome_options=options)
    browser.get("https://en.tripadvisor.com.hk/Attractions")
    # go to city on trip adviser
    browser.find_element_by_xpath('//*[@id="taplc_trip_search_home_attractions_0"]/div[2]/div[1]/div/span/input').send_keys(city_name);
    # time.sleep(5)
    search_attempt = browser.find_element_by_id('SUBMIT_THINGS_TO_DO')
    search_attempt.click()

    try:
        myElem = WebDriverWait(browser, 1000).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[1]/div[2]/a')))
    except TimeoutException:
        print("Loading took too much time!")

    # handle attractions
    attr_list = browser.find_elements_by_xpath("//div[@class='listing_title ']/a")
    links = []
    num_attr = 0
    for i in attr_list:
        try:
            myElem = WebDriverWait(browser, 1000).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ATTR_ENTRY_"]/div[2]/div/div/div[1]/div[2]/a')))
        except TimeoutException:
            print("Loading took too much time!")
        link = i.get_attribute("href")
        attr_text = i.text
        contains_paranthesis = True if '(' in attr_text else False
        if not contains_paranthesis or not is_int(attr_text[attr_text.find('(') + 1]):
            if num_attr < number_attr:
                num_attr += 1
                links.append(link)

    all_attractions = {}
    key = 1
    for i in links:
        print(key)
        browser.get(i)
        attr_name = browser.find_elements_by_id('HEADING')[0].text
        print(attr_name)
        try:
            address = browser.find_elements_by_class_name('street-address')[0].text
        except IndexError as e:
            address = 'Not provided'
        try:
            rating = float(browser.find_elements_by_class_name('overallRating')[0].text)
        except IndexError as e:
            rating = 'Not provided'
        try:
            reviews = int(browser.find_elements_by_class_name('more')[0].text.split()[0].replace(',', ''))
        except IndexError as e:
            reviews = 'Not provided'
        # static now
        duration = 120
        # crawl data -> Trip adviser
        # browser.find_elements_by_xpath('//*[@id="taplc_attraction_detail_listing_0"]/div[1]/div')[0].text
        all_attractions[key] = {}
        all_attractions[key]['name'] = attr_name
        all_attractions[key]['city'] = city_name
        all_attractions[key]["address"] = address
        all_attractions[key]["rating"] = rating
        all_attractions[key]["reviews"] = reviews
        all_attractions[key]["duration"] = duration
        name_without_par = attr_name.split('(')[0] if '(' in attr_name else attr_name
        try:
            all_attractions[key]['description'] = wikipedia.summary(name_without_par)
        except wikipedia.exceptions.DisambiguationError as e:
            all_attractions[key]['description'] = wikipedia.summary(name_without_par)
            print(e.options)
            try:
                all_attractions[key]['description'] = wikipedia.summary(name_without_par + " " + city_name)
            except wikipedia.exceptions.DisambiguationError as ex:
                print(ex.options)
        except wikipedia.exceptions.PageError as e:
            all_attractions[key]['description'] = 'Not provided'
        key += 1
        browser.back()

    print(all_attractions)

    with open(city_name + "_attractions.json", 'w') as out:
        json.dump(all_attractions, out)

    return all_attractions


get_city_attractions('Hong Kong', 15)
get_restaurant_attractions('Hong Kong', 15)

