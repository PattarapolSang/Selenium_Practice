# This file is going to scrape data from the booking website. 
# The data will be stored in a list of dictionaries. Each dictionary will contain the following
# keys: title, link, star, review, price.

from selenium.webdriver.common.by import By
from prettytable import PrettyTable
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    
    def __init__(self, list_of_hotels: list[WebElement]):
        
        self.list_of_hotels = list_of_hotels
        self.output_list = [] 
 
    
    def data_report(self):
        
        for idx, hotel in enumerate(self.list_of_hotels):

            hotel_dict = {}
            print(f'Getting data for hotel {idx+1}')
            hotel_dict['title'] = self.get_title(hotel)
            hotel_dict['link'] = self.get_link(hotel)
            # hotel_dict['star'] = self.get_star(hotel)
            hotel_dict['review'] = self.get_review(hotel)   
            hotel_dict['price'] = self.get_price(hotel)

            self.output_list.append(hotel_dict)
            print('\n\n')
            
        return self.output_list
    
    def get_title(self, element: WebElement):
        try:
            print("\tGetting title")
            title = element.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
            print(f'\tTitle: {title}')
        except Exception as e:
            print(f'Error: {e}')
            title = 'No title'
        return title
    
    def get_link(self, element: WebElement):
        try:
            print("\tGetting link")
            link = element.find_element(By.CSS_SELECTOR, 'a[href^="https://www.booking.com"][data-testid="title-link"]').get_attribute('href')
            print(f'\tLink: {link[:100]}...')
        except Exception as e:
            print(f'Error: {e}')
            link = 'No link'
        return link
    
    def get_star(self, element: WebElement):
        try:
            print("\tGetting star")
            star = element.find_element(By.CSS_SELECTOR, 'div.f97c3d5c2f[tabindex="0"]').get_attribute('aria-label')
            print(f'\tStar: {star}')
        except Exception as e:
            print(f'Error: {e}')
            star = 'No star'
        return star
    
    def get_review(self, element: WebElement):
        try: 
            print("\tGetting review")
            review = element.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"] div[class="a447b19dfd"]').text
            print(f'\tReview: {review}')
        except Exception as e:
            print(f'Error: {e}')
            review = 'No review'
        return review
    
    def get_price(self, element: WebElement):
        try:
            print("\tGetting price")
            price = element.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
            print(f'\tPrice: {price}')
        except Exception as e:
            print(f'Error: {e}')
            price = 'No price'
        return price
    
    def pretty_report(self) -> PrettyTable:
        
        try:
            report = PrettyTable()
            # report.field_names = ['Title', 'Review', 'Price', 'Link']
            print('Entering pretty report')
            print([hotel['title'] for hotel in self.output_list])
            print()
            
            report.add_column('Title', [hotel['title'] for hotel in self.output_list])
            report.add_column('Review', [hotel['review'] for hotel in self.output_list])
            report.add_column('Price', [hotel['price'] for hotel in self.output_list])
            report.add_column('Link', [hotel['link'][:50] for hotel in self.output_list])
        except Exception as e:
            print(f'Error: {e}')
            report = None
        
        return report
    
    
