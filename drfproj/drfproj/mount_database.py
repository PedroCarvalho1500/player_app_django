import sqlite3
import os
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import csv
from parameterized import parameterized
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import Select

soccer_players = [
    "Arthur Gomes",
    "Zarach",
    "Enzo Fern"
]


   





class WebActions():

    def __init__(self) -> None:
        self.serv_obj = Service("chromedriver.exe")
        self.ops=webdriver.ChromeOptions()
        #self.ops.add_argument("--headless")
        self.ops.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,"profile.managed_default_content_settings.video": 2,"adblock": 1})
        
        self.ops.add_argument('--no-sandbox')
        self.driver=webdriver.Chrome(options=self.ops)

                            

        
        self.mywait=WebDriverWait(self.driver,30,poll_frequency=3,ignored_exceptions=[NoSuchElementException,
                                                        ElementNotVisibleException,
                                                        ElementNotSelectableException,
                                                        Exception])


    def wait_element_by(self,locator_type, locator):
        if(locator_type == "CSS"): return self.mywait.until(EC.presence_of_element_located((By.CSS_SELECTOR,locator)))
        else: return self.mywait.until(EC.presence_of_element_located((By.XPATH,locator)))

    def close_ads(self):
        try:
            iframe = self.driver.find_element(By.XPATH, "//iframe[@id='sp_message_iframe_953358']")
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(By.XPATH,"//button[contains(text(),'Accept & continue')]").click()
            self.driver.switch_to.default_content()
        except:
            self.driver.switch_to.default_content()


    def get_to_url(self):
        self.driver.get(url='https://www.transfermarkt.com/')
        self.close_ads()
        time.sleep(3)
        self.close_ads()



    def search_for_player(self,name):
        try:
            self.name = name
            try:
                self.wait_element_by("XPATH","//form[@id='schnellsuche']/input[@placeholder='Enter your search term']")
                self.driver.find_element(By.XPATH,"//form[@id='schnellsuche']/input[@placeholder='Enter your search term']").send_keys(name)
            except:
                self.driver.get(url='https://www.transfermarkt.com/')
                self.close_ads()
                time.sleep(3)
                self.wait_element_by("XPATH","//form[@id='schnellsuche']/input[@placeholder='Enter your search term']")
                self.driver.find_element(By.XPATH,"//form[@id='schnellsuche']/input[@placeholder='Enter your search term']").send_keys(name)
            #finally:
                #self.driver.save_full_page_screenshot('screen.png')
            self.driver.find_element(By.XPATH,"//form[@id='schnellsuche']/input[@alt='search']").click()
            self.close_ads()
            self.driver.find_elements(By.CSS_SELECTOR,"tbody>tr>td[class='hauptlink']>a")[0].click()
            #self.close_ads()
            self.driver.get(url=str(self.driver.current_url).replace('profil','leistungsdaten')+str('/plus/0?saison=ges'))
        except NameError:
            self.driver.close()
            print(NameError)
            
    
    def save_values_into_database(self):
        try:
            db_obj = DB_Actions()
            name = self.name
            team = self.driver.find_element(By.XPATH,"//span[@class='data-header__club']/a").text
            goals = self.driver.find_elements(By.XPATH,"//tfoot/tr/td[@class='zentriert']")[1].text
            assists = self.driver.find_elements(By.XPATH,"//tfoot/tr/td[@class='zentriert']")[2].text
            market_value = str(self.driver.find_element(By.XPATH,"//a[@class='data-header__market-value-wrapper']").text).split()[0]
            db_obj.insert_into_player(name,team,goals,assists,market_value,self.driver)
        except:
            self.driver.close()


    def quit_browser(self):
        self.driver.quit()

class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/player.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        print("DATABASE DISCONNECTED!!!")
        self.conn.close()


    def mountTables(self):
        self.connect_db()
        print("Conectando ao Banco de Dados!")
            
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS player (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                team VARCHAR(100000) NOT NULL,
                total_goals INTEGER NOT NULL,
                total_assists INTEGER NOT NULL,
                market_value VARCHAR(100000) NOT NULL
                )""")
        

        self.conn.commit()
        print("DATABASE CREATED!!!")
        self.disconnect_db()


    def insert_into_player(self,name,team,total_goals,total_assists,market_value,driver):
        self.connect_db()
        self.cursor.execute(""" INSERT INTO player (name,team,total_goals,total_assists,market_value) VALUES(?,?,?,?,?)""", (name,team,total_goals,total_assists,market_value))
        self.conn.commit()
        self.disconnect_db()

class Player():
    def __init__(self) -> None:
        pass


    def get_player_information_save_into_database(self):
        url = "https://transfermarket.p.rapidapi.com/players/get-header-info"

        querystring = {"id":"22323","domain":"de"}

        headers = {
            "X-RapidAPI-Key": os.environ.get('API_KEY'),
            "X-RapidAPI-Host": "transfermarket.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        #print(response.json())
        print(response.json()['data']['player']['name'])
        print(response.json()['data']['player']['marketValue']['value'])



if __name__ == '__main__':
    web = WebActions()
    web.get_to_url()
    for i in soccer_players:
        web.search_for_player(i)
        web.save_values_into_database()
