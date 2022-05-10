from selenium import webdriver
import time
import pause
from datetime import datetime

def open_browser():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get('https://www.instagram.com/accounts/login/')
    time.sleep(4)
    return browser


def login(username, password,browser):
    Web_Username = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input")
    Web_Username.send_keys(username)
    time.sleep(3)
    Web_password = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input")
    Web_password.send_keys(password)
    Web_password.submit()
    time.sleep(5)


def notification(browser):
    try: popup1 = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
    except: pass
    time.sleep(5)
    try: popup2 = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click()
    except: popup2 = browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click()


def Find_message_icon(browser):
    click_msg_icon = browser.find_element_by_class_name("xWeGp")
    click_msg_icon.click()
    time.sleep(3)


def Find_name(name,browser):
    chat = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button")
    chat.click()
    time.sleep(5)
    typename = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input")
    typename.send_keys(name)
    time.sleep(4)
    try: search = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div").click()
    except: search = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div").click()
    time.sleep(4)
    next = browser.find_element_by_class_name("rIacr").click()
    time.sleep(4)


def send_message(message,browser):
    box = browser.find_element_by_tag_name("textarea")
    box.send_keys(message)
    send = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button").click()


def Pinsta(username, password, name, message):
    browser = open_browser()
    try: login(username, password,browser)
    except: return 505
    try: notification(browser)
    except: return 401
    Find_message_icon(browser)
    Find_name(name,browser)
    try:send_message(message,browser)
    except: return 402
    return 202

def S_Pinsta(day,hour,minutes,username, password, name, message):
    pause.until(datetime(2022, 5, int(day), int(hour), int(minutes)))
    return Pinsta(username, password, name, message)
    


