from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
d.get('https://www.google.co.jp/')

assert 'Google' in d.title

input_element = d.find_element_by_name('q')
input_element.send_keys('パイソン')
input_element.send_keys(Keys.RETURN)

assert 'パイソン' in d.title

for h3 in d.find_elements_by_css_selector('a > h3'):
    a = h3.find_element_by_xpath('..')
    print(h3.text)
    print(a.get_attribute('href'))
