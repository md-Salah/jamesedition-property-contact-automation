from sys import exit
import os
import random
import time
from selenium.webdriver.common.keys import Keys

from helpers.scraper import Scraper
from helpers.utility import formatted_time, data_countdown, countdown, execution_time
from helpers.files import read_csv, read_txt, write_to_csv, write_to_txt, read_txt_in_dict, pd_read_csv
from helpers.numbers import formatted_number_with_comma, numbers_within_str, str_to_int

def fill_contact():
    name, email, phone = contact['name'], contact['email'], contact['phone']
    
    if d.find_element('div[class="je2-inquiry__already-sent"]'):
        d.element_click('button[class*="je2-inquiry-mobile-dialog__close"]', delay=1)
        return False
    
    name_input = d.find_element('input[name="name"]')
    if name_input and name_input.get_attribute('value') != name:
        d.element_send_keys(name, element=name_input)
        
        email_input = d.find_element('input[name="email"]')
        if email_input and 'disabled' not in email_input.get_attribute('class'):
            d.element_send_keys(email, element=email_input)

    # Submit button
    d.element_click('div[class="je2-inquiry__submit"] button')
    d.sleep(4, 5)
    
    success = d.find_element('div[class="je2-thank-you-dialog _success"]')
    if success:
        d.element_click('button', ref_element=success)
        return True
    else:
        return False
    
    
def main():
    search_location = 'California, PA, United States'
    d.go_to_page(url)
    
    #search
    d.sleep(1.5)
    d.element_send_keys(search_location, 'input[name="search"]')
    d.sleep(1.5)
    d.element_click('div[class*="search-field__suggestion-item"]')
    
    base_url = d.driver.current_url
    
    count, page = 0, 1
    while True:
        d.sleep(3, 4, True)
        contact_btns = d.find_elements('div[class="js-contact-button"]', loop_count=4)
        if len(contact_btns) == 0:
            break
                
        for btn in contact_btns:
            d.element_click(element=btn)
            success = fill_contact()
            if success:
                count = count + 1
                data_countdown(f'{count} contacts filled')

        # Next page
        page += 1
        next_page_url = base_url + f'?page={page}'
        d.go_to_page(next_page_url)

if __name__ == "__main__":
    START_TIME = time.time()


    # Global variables
    contact = read_txt_in_dict('inputs/contact_info.txt', '=')
    url = 'https://www.jamesedition.com/real_estate'
    d = Scraper(url, exit_on_missing_element=False, profile=contact['email'][:6])
    d.print_executable_path()
    
    main()
    
    # Footer for reporting
    execution_time(START_TIME)

    # Finally Close the browser
    input('Press any key to exit the browser...')
    d.driver.close()
