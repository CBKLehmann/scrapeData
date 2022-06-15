from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime


if __name__ == '__main__':

    print(datetime.now())

    datas = []
    loop = True
    counter = 0

    browser = webdriver.Chrome()
    new_browser = webdriver.Chrome()
    browser.get('https://www.pflegeausbildung.net/no_cache/alles-zur-ausbildung/uebersicht-pflegeschulen.html')

    display_amount = browser.find_element(By.NAME, 'tx_bafzaaltenpflegeschulen_demap[itemsPerPage]')
    display_amount.send_keys(100)
    display_amount.send_keys(Keys.RETURN)
    display_amount.click()
    submit = browser.find_elements(By.CLASS_NAME, 'form-control')
    submit[0].click()
    time.sleep(1)
    while loop:
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
                'Straße': infos[1],
                'PLZ/Ort': infos[2],
                'Telefon': telefon,
                'EMail': email,
                'Web': web,
                'Abschlüsse': ausbildungDetails[0].text.split('\n'),
                'Teilzeitausbildung': teilzeit,
                'Zertifiziert': zertifiziert
            }
            datas.append(data)

        try:
            browser.find_element(By.CLASS_NAME, 'next').click()
        except:
            loop = False
        finally:
            counter += 1

    print('##########################################')
    print(len(datas))
    for entry in datas:
        print(entry)
    print('##########################################')
    print(datetime.now())

    new_browser.quit()
    browser.quit()