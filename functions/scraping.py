from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.database import write_db
import sys
import json


def collect_data(contact, details, today):
    telefon = 'N/A'
    web = 'N/A'
    email = 'N/A'
    plz = 'N/A'
    street = 'N/A'
    city = 'N/A'
    krs_code = 'N/A'

    for content in contact:
        if '<p>' in content.get_attribute('innerHTML'):
            p = content.find_element(By.TAG_NAME, 'p')
            infos = (p.get_attribute('innerText').split('\n'))
            street = infos[1]
            plz = infos[2].split(' ')[0]
            city = infos[2].split(' ')[1]
        else:
            children = (content.find_element(By.TAG_NAME, 'ul').get_property('children'))
            for child in children:
                inner_text = (child.get_attribute('innerText').split('\n'))
                if 'E-Mail senden' in inner_text:
                    email = child.find_element(By.TAG_NAME, 'a').get_property('pathname')
                elif 'Tel.:' in inner_text:
                    telefon = inner_text[1]
                elif 'Web:' in inner_text:
                    web = inner_text[1]

    ausbildungsdetails = details.find_elements(By.CLASS_NAME, 'ausbildungDetails')
    zertifiziert_element = details.find_elements(By.CLASS_NAME, 'azavZertifiziert')

    if len(ausbildungsdetails) > 1:
        teilzeit = ausbildungsdetails[1].text
    else:
        teilzeit = 'N/A'

    if len(zertifiziert_element) == 1:
        zertifiziert = zertifiziert_element[0].text
    else:
        zertifiziert = 'N/A'

    try:
        with open('georef-germany-postleitzahl.json', 'r', encoding='utf-8') as f:
            for entry in json.loads(f.read()):
                if entry['fields']['plz_code'] == plz:
                    krs_code = entry['fields']['krs_code']
                    break
    except Exception as err:
        print(plz)
        print(err)

    data = {
        'name': details.find_element(By.TAG_NAME, 'h2').text,
        'street': street,
        'postcode': plz,
        'city': city,
        'telefon': telefon,
        'email': email,
        'web': web,
        'degree': ausbildungsdetails[0].text.split('\n'),
        'parttime_education': teilzeit,
        'certificate': zertifiziert,
        'district_code': krs_code,
        'inserted': today,
        'updated': today
    }

    return data


def scrape_page_care_dev(today):
    counter = 1
    count = 0

    browser = webdriver.Chrome()
    new_browser = webdriver.Chrome()
    browser.get('https://www.pflegeausbildung.net/no_cache/alles-zur-ausbildung/uebersicht-pflegeschulen.html')

    while count <= 3:
        count += 1
        data_arr = []
        list_schools = browser.find_element(By.CLASS_NAME, 'altenpflegeschulen')
        single_items = list_schools.find_elements(By.CLASS_NAME, 'showSingleItem')
        links = [item.get_attribute('href') for item in single_items]
        for item in links:
            if counter <= 500:
                new_browser.get(item)
                data_arr.append(collect_data(
                    contact=new_browser.find_elements(By.CLASS_NAME, 'col-sm-6'),
                    details=new_browser.find_element(By.CLASS_NAME, 'detailView'),
                    today=today))
                counter += 1

        try:
            session = write_db(data_arr, 'pflege_ausbildung')
            browser.find_element(By.CLASS_NAME, 'next').click()
        except Exception as main_err:
            print('Something happened while changing the page')
            print(sys.exc_info())
            print(main_err)
            loop = False

    new_browser.quit()
    browser.quit()

    return session, data_arr


def scrape_page_care(today):
    data_arr = []
    loop = True

    browser = webdriver.Chrome()
    new_browser = webdriver.Chrome()
    browser.get('https://www.pflegeausbildung.net/no_cache/alles-zur-ausbildung/uebersicht-pflegeschulen.html')

    while loop:
        list_schools = browser.find_element(By.CLASS_NAME, 'altenpflegeschulen')
        single_items = list_schools.find_elements(By.CLASS_NAME, 'showSingleItem')
        links = [item.get_attribute('href') for item in single_items]
        for item in links:
            new_browser.get(item)
            data_arr.append(collect_data(
                contact=new_browser.find_elements(By.CLASS_NAME, 'col-sm-6'),
                details=new_browser.find_element(By.CLASS_NAME, 'detailView'),
                today=today))

        try:
            browser.find_element(By.CLASS_NAME, 'next').click()
        except Exception as main_err:
            print('Something happened while changing the page')
            print(sys.exc_info())
            print(main_err)
            loop = False

    session = write_db(data_arr, 'pflege_ausbildung')
    new_browser.quit()
    browser.quit()

    return session, data_arr


def call_scrape_function(today, dev):
    if dev:
        return scrape_page_care_dev(today)
    else:
        return scrape_page_care(today)