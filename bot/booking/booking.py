from types import TracebackType
from typing import Type
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from booking.booking_report import BookingReport

import booking.constant as const 
import time



# Rest of the code

class Booking(webdriver.Chrome):

    def __init__(self, driver_path: str = const.CHROME_DRIVER_PATH, teardown: bool =False):
        self.driver_path = driver_path
        self.teardown = teardown
        
        self.settingcheck= {'currency': False, 'location': False, 'date': False, 'occupancy': False}
        self.output_list = []
        
        self.options = Options()
        self.options.add_experimental_option('detach', True)
        self.options.add_argument('--log-level=1')
        super(Booking, self).__init__(options= self.options , keep_alive=True)
        self.implicitly_wait(10) 
        self.maximize_window()
        
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        print(f'Tear down: {self.teardown}')
        if self.teardown:
            print("Quitting the driver")
            self.quit()
        else:
            print("Leaving the driver open")
        
    def land_first_page(self):
        self.get(const.BASE_URL)
        
        try:
            ignore_signin = self.find_element(By.CSS_SELECTOR, 'span.c3d4b5d161')
            print("Ignore Signin.....")
            ignore_signin.click()
        except:
            pass
        
    def chang_currency(self, currency='CNY'): 
        
        current_currency  = self.find_element(By.CSS_SELECTOR, 'span.eed450ee2f')
        current_currency.click()
        
        list_currency = self.find_elements(By.CSS_SELECTOR, 'div.b284c0e8fc ')
        print(f'Found {len(list_currency)} currencies')
        
        for idx, coin in enumerate(list_currency):
            # print(f'{idx + 1} - {coin.text}')
            if coin.text == currency:
                print(f"Clicking on {coin.text}")
                coin.click()
                print("Currency changed")
                break
            
        WebDriverWait(self, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.settingcheck['currency'] = True
    
    def select_destination(self, destination: str):
        search_field = self.find_element(By.CSS_SELECTOR, 'input.a263b5b5e8')
        search_field.send_keys(destination)
        
        WebDriverWait(self, 10).until(EC.text_to_be_present_in_element(
            [By.CSS_SELECTOR, 'div[class="ecd0590af5 b2bcede8b1"]'], destination))
        
        print("Selecting the first option....")
        list_search = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
        list_search.click()
        self.settingcheck['location'] = True
        
    def select_date(self, checkin_date: str, checkout_date: str):
        
        WebDriverWait(self, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'nav[data-testid="datepicker-tabs"]')))
        checkin = self.find_element(By.CSS_SELECTOR, f'td span[data-date="{checkin_date}"]')
        checkin.click()
        
        checkout = self.find_element(By.CSS_SELECTOR, f'td span[data-date="{checkout_date}"]')
        checkout.click()   
        self.settingcheck['date'] = True    
    
    def select_occupancy(self, adults:int = 1, children:int = 0, rooms:int = 1, children_age:int = 1):
        
        list_occupancy = [adults, children, rooms]
        self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]').click()
        
        list_inputs = self.find_elements(By.CSS_SELECTOR, 'div.fa3b3e32a3')
        print(f'Found {len(list_inputs)} inputs')
        
        for idx, number in enumerate(list_inputs):
                        
            try:
                current_number = int(number.find_element(
                    By.CSS_SELECTOR, 'input[aria-valuenow]').get_attribute("aria-valuenow"))
            except:
                print("Strange error --> Change location")
                number = self.find_element(By.CSS_SELECTOR, 'div.bb240b4de9')
                current_number = 0
            
            button = number.find_elements(By.CSS_SELECTOR, 'button[tabindex="-1"]')
            while current_number != list_occupancy[idx]:
                
                print(f'Looping {current_number} // {list_occupancy[idx]}')
                
                if current_number < list_occupancy[idx]:
                    print("Clicking +")
                    plus_button = button[1]
                    plus_button.click()

                elif current_number > list_occupancy[idx]:
                    print("Clicking -")
                    minus_button = button[0]
                    minus_button.click()        
                
                
                current_number = int(number.find_element(
                    By.CSS_SELECTOR, 'input[aria-valuenow]').get_attribute("aria-valuenow"))

        if children > 0:  
            
            select_children = Select(self.find_element(By.CSS_SELECTOR, 'select[class="d9a1712785"]'))
            select_children.select_by_value(str(children_age))
                
        pass
            
        self.settingcheck['occupancy'] = True
    
    def commit_form(self):
        
        if all(self.settingcheck.values()):
            self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            print("Form submitted Please wait for 10 seconds")
        else:
            print("Form not completed")
            for key, value in self.settingcheck.items():
                if not value:
                    print(f"Missing: {key}")
        
    def data_scrape(self, report_table:bool = False) -> list:
        
        WebDriverWait(self, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        for _ in range(10):
            time.sleep(1)
            print(f"Load {_} ...")
        
        property_list = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card-container"]')
        print(f'\nFound {len(property_list)} properties') 
        
        print("***** Report data ******\n\n")
        
        try:
            report = BookingReport(property_list)
            self.output_list = report.data_report()
            
            if report_table:
                print("***** Table data ******\n\n")
                table = report.pretty_report()
                print(table)
                print("***** End of Table data ******\n\n")
            
        except Exception as e:
            print("Error in report")    
            print(f'Error: {e}')
        
        # for idx, property in enumerate(property_list):
            
        #     try:
        #         title = property.find_element(
        #             By.CSS_SELECTOR, 'div[data-testid="title"]').text
        #         link  = property.find_element(
        #             By.CSS_SELECTOR, 'a[href^="https://www.booking.com"][data-testid="title-link"]').get_attribute("href")
        #         # star  = property.find_element(
        #         #     By.CSS_SELECTOR, 'div.f97c3d5c2f[tabindex="0"]').get_attribute("aria-label")
        #         review = property.find_element(
        #             By.CSS_SELECTOR, 'div[data-testid="review-score"] div[class="a447b19dfd"]').text
        #         price = property.find_element(
        #             By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text  
            
        #     except Exception as e:
        #         print(f'Error: {e}')
        #         title = ''
        #         link  = ''
        #         # star  = ''
        #         review = ''
        #         price = ''
            
        #     print(f'{idx + 1} - {title}')
        #     print(f'Review: {review}')
        #     # print(f'Star: {star}')
        #     print(f'Price: {price}')
        #     print(f'Link: {link[:70]}...\n\n')
            
        #     self.output_list.append({
        #             'title': title,
        #             'link': link,
        #             # 'star': star,
        #             'review': review,
        #             'price': price
        #         })
                
        # print("Data scraped")
        # print(self.output_list)
        return self.output_list
                
        pass
    
        
        

    

            
        
        
        
        


    
    