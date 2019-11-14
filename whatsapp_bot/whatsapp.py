from selenium import webdriver

driver = webdriver.Chrome('C:/Users/ARPIT/Downloads/asdfg/chromedriver')
driver.get('https://web.whatsapp.com/')

name = "Devash Bhai Sanghvi"
msg = "this message send from python script :)"
count = 1

input('Enter anything after scanning QR code')

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()

msg_box = driver.find_element_by_class_name('_3u328')

for i in range(count):
    msg_box.send_keys(msg)
    button = driver.find_element_by_class_name('_3M-N-')
    button.click()