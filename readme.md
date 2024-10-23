
# Booking Automation Script

This project automates the process of searching for hotels on the Booking.com website. The automation script interacts with the website, searches for hotels based on user inputs, scrapes hotel data, and displays the results in a structured format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Logging](#logging)
- [Requirements](#requirements)

## Installation

Before running the script, make sure you have the required dependencies installed:

1. Install the necessary Python packages:
   ```bash
   pip install selenium prettytable
   ```

2. Download the Chrome WebDriver that matches your Chrome version and place it in the appropriate directory:
   ```bash
   https://sites.google.com/a/chromium.org/chromedriver/downloads
   ```

3. Update the `constant.py` file with the correct path to your ChromeDriver:
   ```python
   CHROME_DRIVER_PATH = 'path_to_your_chromedriver'
   ```

## Usage

1. **Running the Script**:

   The `main.py` script is the entry point. It launches a browser, opens the Booking.com website, and interacts with it according to the user input.

   ```bash
   python main.py
   ```

2. **User Inputs**:
   The script will prompt you for the following details:
   - Destination (e.g., "New York")
   - Departure date
   - Return date
   - Number of adults, children, rooms, and the age of the children

3. **Hotel Data Scraping**:
   After the form is filled, the script will scrape the hotel data and display it in a tabular format. The scraped data includes:
   - Hotel title
   - Hotel review score
   - Price per night
   - Link to the hotel on Booking.com

## File Structure

- `main.py`: The main script that orchestrates the entire process, interacting with the user for input and then launching the Booking.com automation.
- `booking.py`: This file contains the `Booking` class, which handles the interaction with the Booking.com website (e.g., filling the form, selecting the destination, dates, occupancy, etc.).
- `booking_report.py`: Contains the `BookingReport` class that scrapes and organizes the hotel data from Booking.com.
- `constant.py`: Holds configuration constants, such as the ChromeDriver path and the Booking.com URL.

## Logging

The script outputs relevant information such as:
- Status of form submission
- Number of hotels found
- Scraped hotel data (titles, reviews, prices, etc.)

## Requirements

- Python 3.x
- Selenium WebDriver
- Google Chrome (ensure that your Chrome version matches the ChromeDriver version)
- ChromeDriver (download it from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads))

## Future Improvements

- Add error handling to manage cases where elements are not found on the page.
- Improve data scraping to include more hotel details (e.g., star rating).
- Enhance the user interface to allow input via a graphical interface.
