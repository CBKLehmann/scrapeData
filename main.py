from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import json
from os.path import exists
import sys
from functions.database import write_db, create_table


if __name__ == '__main__':

    create_table()

    today = str(datetime.now()).split('.')[0]
    # today = str(datetime.now() + timedelta(days=72, hours=3)).split('.')[0]
    print(datetime.now())

    datas_arr = []
    loop = True
    counter = 1
    count = 0

    browser = webdriver.Chrome()
    new_browser = webdriver.Chrome()
    browser.get('https://www.pflegeausbildung.net/no_cache/alles-zur-ausbildung/uebersicht-pflegeschulen.html')

    # while loop: # Activate for Production
    while count <= 0:  # Deactivate for Production
        count += 1
        list_schools = browser.find_element(By.CLASS_NAME, 'altenpflegeschulen')
        singleItems = list_schools.find_elements(By.CLASS_NAME, 'showSingleItem')
        links = [item.get_attribute('href') for item in singleItems]
        for item in links:
            if counter <= 5:  # Deactivate for Production
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

                with open('georef-germany-postleitzahl.json', 'r', encoding='utf-8') as f:
                    for entry in json.loads(f.read()):
                        if entry['fields']['plz_code'] == plz:
                            krs_code = entry['fields']['krs_code']

                data = {
                    'name': details.find_element(By.TAG_NAME, 'h2').text,
                    'street': street,
                    'postcode': plz,
                    'city': city,
                    'telefon': telefon,
                    'email': email,
                    'web': web,
                    'degree': ausbildungDetails[0].text.split('\n'),
                    'parttime_education': teilzeit,
                    'certificate': zertifiziert,
                    'district_code': krs_code,
                    'inserted': today,
                    'updated': today
                }

                datas_arr.append(data)
                counter += 1

        session = write_db(datas_arr, 'pflege_ausbildung')

        try:
            browser.find_element(By.CLASS_NAME, 'next').click()
        except Exception as main_err:
            print('Something happened in db_connect')
            print(sys.exc_info())
            print(main_err)
            loop = False
        finally:
            new_browser.quit()
            browser.quit()

    if exists('data.json'):
        delete_values = []
        with open('data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
            raw_content = content
            content_index = 0
            print('######################################')
            while content_index < len(raw_content):
                data_index = 0
                while data_index < len(datas_arr):
                    if datas_arr[data_index]['name'] == raw_content[content_index]['name']:
                        for data_key in datas_arr[data_index]:
                            if not data_key == 'inserted':
                                content[content.index(raw_content[content_index])][data_key] = datas_arr[data_index][data_key]
                        content[content.index(raw_content[content_index])]['updated'] = today
                    data_index += 1
                content_index += 1
        #         found = False
        #         while not found:
        #             for data in datas_arr:
        #                 if data['name'] == raw_content[index]['name']:
        #                     for data_key in data:
        #                         if not data_key == 'inserted':
        #                             content[content.index(raw_content[index])][data_key] = data[data_key]
        #                     content[content.index(raw_content[index])]['updated'] = today
        #                     found = True
        #         if not found:
        #             content.pop(content.index(raw_content[index]))
        #             delete_values.append(raw_content[index])
        # print(len(delete_values))
        # print(len(content))






        # with open('data.json', 'w', encoding='utf-8') as nf:
        #     json.dump(content, nf, ensure_ascii=False, indent=4)
    else:
        for data in datas_arr:
            data['inserted'] = today
            data['updated'] = today
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(datas_arr, f, ensure_ascii=False, indent=4)
    print(datetime.now())
