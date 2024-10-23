from booking.booking import Booking
import time

# def main():
#     booking = Booking()
#     booking.land_first_page()
#     time.sleep(5)
#     # booking.close()

# if __name__ == "__main__":
#     main()

with Booking(teardown=True) as bot:
    
    bot.land_first_page()
    bot.chang_currency('USD')
    bot.select_destination(input('Where do you want to go?')) # 'New York'
    bot.select_date(input("When do you want to departure?"), input("When do you want to arrive?")) #'2024-08-01', '2024-08-03'
    bot.select_occupancy( 
                         int(input("How many adult: ")), 
                         int(input('How many children: ')), 
                         int(input('How many room: ')), 
                         int(input('How old children: ')) 
                         ) # adults = 5, children = 1, rooms = 5, children_age = 5
    bot.commit_form()
    
    hotel_data = bot.data_scrape(report_table=True)
    
    # print("Printing hotel data")
    # print(f'Found {len(hotel_data)} hotels')
    # print(f'Label: {hotel_data[0].keys()}')
    
    # for hotel in hotel_data:
    #     print(hotel)
    
    print("Exit ------->")