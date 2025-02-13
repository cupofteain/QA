import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
import time
import re
import random
import os
import datetime

# Настройка драйвера
options = Options()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(), options=options)

try:
    driver.get("https://store-dev.ecar.kz/")
    time.sleep(3)
    driver.maximize_window()

    time.sleep(3)
    # Проверка, открытия  меню выбора города
    try:
        city_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class, 'CitySelectModal_cityInitialModal__CYQei')]",
                )
            )
        )
        print("Меню выбора города появилось.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(1)
    # Клик на кнопку "Да, всё верно", в меню выбора города
    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'CitySelectModal_actionButton')]",
                )
            )
        )
        confirm_button.click()
        print("Кнопка 'Да, всё верно' нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        b2b_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mainSection"]/header[1]/div/div[3]/div/button'))
        )
        b2b_profile.click()
        print("Кнопка Вход - нажата")
    except Exception as e:
        print(f"Ошибка в нажатие на кнопку - Вход {e}")

    time.sleep(3)
 

    try:
        container = driver.find_element(By.CLASS_NAME, "LoginFields_loginFields__xkHSq")
        
        input_element = container.find_element(By.CLASS_NAME, "Input_input__BbM8T")

        actions = ActionChains(driver)
        actions.move_to_element(input_element).perform()
        time.sleep(1)

        input_element.click()
        time.sleep(0.5)  

        input_element.send_keys("sales1@supershina.kz")

        print("email введен")

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(3)

    try:
        container = driver.find_element(By.CLASS_NAME, "LoginFields_loginFields__xkHSq")
        
        input_element = container.find_element(By.CLASS_NAME, "styles_textField__TO8xW")

        actions = ActionChains(driver)
        actions.move_to_element(input_element).perform()
        time.sleep(1)

        input_element.click()
        time.sleep(0.5)  

        input_element.send_keys("Alm12345")

        print("password введен")

    except Exception as e:
        print(f"Ошибка: {e}")

    try:
        container = driver.find_element(By.CLASS_NAME, "LoginFields_loginFields__xkHSq")
        
        input_element = container.find_element(By.CLASS_NAME, "Button_medium__lxzcc")

        actions = ActionChains(driver)
        actions.move_to_element(input_element).perform()
        time.sleep(1)

        input_element.click()
        time.sleep(0.5)  

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(15)
    driver.execute_script("window.scrollBy(0, 400);") #scroll
    time.sleep(5)
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                '//*[@id="main-content"]/div/div/div[4]/div[2]/main/div[1]/div[3]/button'
            ))
        )

        actions = ActionChains(driver)

        actions.move_to_element(button).click().perform()

        print("Мышь наведена и выполнен двойной клик!")

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(5)

    # Скрол к корзине
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

     # Нажатие на кнопку "Корзина"
    try:
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Корзина']"))
        )
        cart_button.click()
        print("Переход в корзину выполнен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Клик на кнопку "Переход к оформению"
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Перейти к оформлению']"))
        )

        checkout_button.click()
        print("Нажата кнопка 'Перейти к оформлению'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(5)

finally:
    time.sleep(5)
    driver.quit()