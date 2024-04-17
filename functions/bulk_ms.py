import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By


def bulk_ms(filename):
    # dataframe = pd.read_excel(
    #     f"./src/tables/{filename}.xlsx",
    #     header=2
    # )
    # for i in range(dataframe.shape[0]):
    #     print(dataframe.loc[i])

    driver = webdriver.Chrome('D:\chromedriver')
    driver.get('https://www.terranus.de/bauliche-vorgaben-fuer-pflegeheime/')
    table = driver.find_element(By.ID, 'popups')
    popups = table.find_elements(By.CLASS_NAME, 'popup')
    for popup in popups:
        federal_state = popup.find_element(By.TAG_NAME, 'h3')
        print(federal_state.get_attribute('textContent'))
    driver.quit()
