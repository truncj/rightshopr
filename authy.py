from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils import read_json

creds = read_json('creds')

opts = Options()
# opts.headless = True

def authenticate():
    cookies = ''
    kv_cookies = ''

    try:
        driver = webdriver.Chrome(options=opts)

        # load home page
        driver.get('https://shop.shoprite.com/')
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'ShopperIdentityBtn')))
        driver.find_element_by_id('ShopperIdentityBtn').click()
        WebDriverWait(driver, 10).until(expected_conditions.number_of_windows_to_be(2))

        # switch to login window
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, 'Email')))
        driver.find_element_by_id('Email').send_keys(creds['username'])
        driver.find_element_by_id('Password').send_keys(creds['password'])
        driver.find_element_by_id('SignIn').click()

        # back to main window
        driver.switch_to.window(driver.window_handles[0])
        cookies = driver.get_cookies()
    except Exception as e:
        print(f'Error on authentication: {e}')
    finally:
        driver.quit()

    for cookie in cookies:
        kv_cookies += f'{cookie["name"] }={cookie["value"]};'

    headers = {
        'authority': "shop.shoprite.com",
        'accept': "*/*",
        'sec-fetch-dest': "empty",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'origin': "https://shop.shoprite.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'referer': "https://shop.shoprite.com/store/c551123799/reserve-timeslot",
        'accept-language': "en-US,en;q=0.9",
        'cookie': f'{kv_cookies}',
        'cache-control': "no-cache",
    }

    return headers