from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np

# Initialize the WebDriver (e.g., ChromeDriver)


# Define the start date
#start_date = datetime(2024, 11, 10)
start_date = datetime.now()
# Get the current date
current_date = datetime.now()
#current_date = datetime(2024, 10, 21)
# Generate the range of dates
date_range = []
current = start_date
df = pd.read_csv('notebook/final_data.csv')
last_date = df.tail(1).to_dict(orient='records')
if last_date[0]['Date'] == current.strftime('%m/%d/%Y'):
   print("Already Scrapped!!!! ")
else: 
    while current <= current_date:
        date_range.append(current.strftime('%m/%d/%Y'))
        current += timedelta(days=1)

# Initialize an empty DataFrame
driver = webdriver.Chrome()
# Open the search page
driver.get('https://kalimatimarket.gov.np/price')
i = 0
# Loop through each date and fetch data
print(date_range)
while i < len(date_range):
    try:
        date = date_range[i]
        # Find the search input field and enter the search term
        date_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'datePricing')))
        date_input.clear()  # Clear any existing input
        date_input.send_keys(date)  # Replace with the desired date

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.comment-btn')))
        try:
            submit_button.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", submit_button)

        # Wait for the results to load
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'commodityPriceParticular')))

        # Parse the results
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Fetch and store data in the DataFrame
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells:
                commodity = cells[0].text if len(cells) > 0 else np.nan
                unit = cells[1].text if len(cells) > 1 else np.nan
                minimum = cells[2].text if len(cells) > 2 else np.nan
                maximum = cells[3].text if len(cells) > 3 else np.nan
                average = cells[4].text if len(cells) > 4 else np.nan
               
                if commodity == 'टेबलमा डाटा उपलब्ध भएन':
                    print(f'In Date: {date} data not found') 
                    print(f'Waiting for data .....')
                    time.sleep(600)
                    
                    
                else:
                    
                    new_row = pd.DataFrame({'Date': [date], 'Commodity': [commodity], 'Unit': [unit], 'Minimum': [minimum], 'Maximum': [maximum], 'Average': [average]})
                    df = pd.concat([df, new_row], ignore_index=True)
        
        if commodity != 'टेबलमा डाटा उपलब्ध भएन':
            i += 1
        

    except TimeoutException:
        print(f"Timeout occurred for date: {date}")
    except NoSuchElementException:
        print(f"Element not found for date: {date}")
    except Exception as e:
        print(f"An error occurred for date: {date}. Error: {e}")

# Close the browser
driver.quit()

# Optionally, save the DataFrame to a CSV file
df.to_csv('notebook/final_data.csv', index=False)
