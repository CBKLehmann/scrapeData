from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import json
from os.path import exists

if __name__ == '__main__':

    today = str(datetime.now()).split('.')[0]
    print(datetime.now())

    datas = {}
    loop = True
    counter = 1
    count = 0

    browser = webdriver.Chrome()
    new_browser = webdriver.Chrome()
    browser.get('https://www.pflegeausbildung.net/no_cache/alles-zur-ausbildung/uebersicht-pflegeschulen.html')

    # while loop:
    while count == 0:
        count += 1
        list_schools = browser.find_element(By.CLASS_NAME, 'altenpflegeschulen')
        singleItems = list_schools.find_elements(By.CLASS_NAME, 'showSingleItem')
        links = [item.get_attribute('href') for item in singleItems]
        for item in links:
            new_browser.get(item)
            details = new_browser.find_element(By.CLASS_NAME, 'detailView')
            contact = new_browser.find_elements(By.CLASS_NAME, 'col-sm-6')
            infos = None
            contacts = None
            telefon = 'N/A'
            web = 'N/A'
            email = 'N/A'

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
                        innerText = (child.get_attribute('innerText').split('\n'))
                        if 'E-Mail senden' in innerText:
                            email = child.find_element(By.TAG_NAME, 'a').get_property('pathname')
                        elif 'Tel.:' in innerText:
                            telefon = innerText[1]
                        elif 'Web:' in innerText:
                            web = innerText[1]

            ausbildungDetails = details.find_elements(By.CLASS_NAME, 'ausbildungDetails')
            zertifiziertElement = details.find_elements(By.CLASS_NAME, 'azavZertifiziert')

            if len(ausbildungDetails) > 1:
                teilzeit = ausbildungDetails[1].text
            else:
                teilzeit = 'N/A'

            if len(zertifiziertElement) == 1:
                zertifiziert = zertifiziertElement[0].text
            else:
                zertifiziert = 'N/A'

            data = {
                'Name': details.find_element(By.TAG_NAME, 'h2').text,
                'Straße': street,
                'PLZ': plz,
                'Stadt': city,
                'Telefon': telefon,
                'EMail': email,
                'Web': web,
                'Abschlüsse': ausbildungDetails[0].text.split('\n'),
                'Teilzeitausbildung': teilzeit,
                'Zertifiziert': zertifiziert
            }
            datas[f'{counter}'] = data
            counter += 1
        try:
            browser.find_element(By.CLASS_NAME, 'next').click()
        except Exception:
            print(Exception)
            loop = False

    print('##########################################')
    print(len(datas))
    if exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
            for data in datas:
                for key in content:
                    if datas[data]['Name'] == content[key]['Name']:
                        for data_key in datas[data]:
                            content[key][data_key] = datas[data][data_key]
                        content[data]['Überprüft'] = today
        with open('data.json', 'w', encoding='utf-8') as nf:
            json.dump(content, nf, ensure_ascii=False, indent=4)
    else:
        for data in datas:
            datas[data]['Eintrag'] = today
            datas[data]['Überprüft'] = today
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(datas, f, ensure_ascii=False, indent=4)
    print('##########################################')
    print(datetime.now())

    new_browser.quit()
    browser.quit()
