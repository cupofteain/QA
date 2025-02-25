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
import telebot

# Настройка драйвера
options = Options()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(), options=options)

BOT_TOKEN = "7788445219:AAFgKPq6CNIIqKsW3uwkDoAWXZbJ4VMBxAU"
CHAT_ID = "5426311862"


def send_screenshot_to_telegram(file_path):
    """Отправляет скриншот в Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(file_path, "rb") as photo:
        response = requests.post(
            url, data={"chat_id": CHAT_ID}, files={"photo": photo}
        )
    if response.status_code == 200:
        print("Скриншот успешно отправлен в Telegram!")
    else:
        print(f"Ошибка при отправке скриншота в Telegram: {response.text}")

def send_error_to_telegram(error_message, screenshot_path):
    """Отправляет ошибку и скриншот в Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url, data={"chat_id": CHAT_ID, "text": error_message}
        )
        if response.status_code == 200:
            print("Ошибка успешно отправлена в Telegram!")
        else:
            print(f"Ошибка при отправке ошибки в Telegram: {response.text}")
        
        # Отправляем скриншот после ошибки
        send_screenshot_to_telegram(screenshot_path)
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке ошибки в Telegram: {e}")

    screenshot_folder = "screenshots"
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

try:
    driver.get("https://front-qa.ecar.kz/")
    time.sleep(3)
    driver.maximize_window()

    time.sleep(3)
    # Проверка, открытия меню выбора города
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
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)
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
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Нажатие на кнопку "Подобрать диски"
    try:
        select_disks_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[text()='Подобрать диски']",
                )
            )
        )
        select_disks_button.click()
        print("Кнопка - Подобрать диски нажата.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(3)
    driver.execute_script("window.scrollBy(0, 50);")
    time.sleep(1)

    # Клик на кнопку "Добавить в корзину"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            product_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "ProductCardAlternative_addCart__CCEoW")
                )
            )

            if product_buttons:
                random_button = random.choice(product_buttons)

                try:
                    random_button.click()
                    print("Случайная кнопка 'Добавить в корзину' нажата.")
                    break
                except Exception as e:
                    driver.execute_script("arguments[0].click();", random_button)
                    print("Случайная кнопка 'Добавить в корзину' нажата.")
                    break
            else:
                print("Ошибка: кнопки 'Добавить в корзину' не найдены.")
                break

        except StaleElementReferenceException:
            print(
                f"Попытка {attempt + 1} из {max_retries}: элемент устарел, пробуем снова..."
            )

    else:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)
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
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Клик на кнопку "Переход к оформению"
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Перейти к оформлению']"))
        )

        checkout_button.click()
        print("Нажата кнопка 'Перейти к оформлению'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Ввод телефона
    try:
        phone_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "phoneNumber"))
        )

        phone_input.click()

        phone_input.send_keys("7075007554")
        print("Номер телефона введен.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Ввод имени
    try:
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "userName"))
        )

        name_input.click()

        name_input.send_keys("Eldar")
        print("Имя пользователя введено.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)

    # Клик на кнопку "Продолжить"
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Продолжить']"))
        )

        next_btn.click()
        print("Кнопка продолжить нажата.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)

    # Выбор способа доставки
    try:
        client_green_zone = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shipmentServiceId"))
        )
        client_green_zone.click()
        print("Кнопка - Выбора доставки нажата")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)

    # Скрол к инпуту Улицы
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    try:
        shipment_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "shipmentAddress"))
        )
        shipment_address.send_keys("Там 32/2")
        print("Улица введена.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(2)

    # Скрол к выбору времени доставки
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Выбор дня доставки
    try:
        days = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "Option_container__tT29F")
            )
        )

        # Фильтруем элементы, исключая те, которые содержат текст "Сегодня2"
        valid_days = [day for day in days if "Сегодня" not in day.text]

        if valid_days:
            random_day = random.choice(valid_days)
            random_day.click()
            print("Случайный день недели успешно выбран.")
        else:
            print("Ошибка: элементы для выбора дня недели не найдены.")
            
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)
        
    # Выбор времени доставки
    try:
        time_slots = [
            "00:00 - 01:00",
            "10:00 - 14:00",
            "14:00 - 19:00",
            "15:00 - 19:00",
            "17:00 - 18:00",
            "18:00 - 20:30",
            "19:00 - 21:00",
        ]

        target_time = random.choice(time_slots)
        print(f"Выбрано время: {target_time}")

        time_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[text()='{target_time}']"))
        )

        ActionChains(driver).move_to_element(time_element).click().perform()
        print(f"Элемент с временем {target_time} успешно нажат.")

    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Клик на кнопку "Продолжить"
    next_btn_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Продолжить']"))
    )

    next_btn_2.click()
    print("Кнопка продолжить нажата.")
    time.sleep(2)

    # Выбор способа оплаты
    try:
        online_payment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(@class, 'Subtitle_root__LPeeH') and contains(@class, 'Subtitle_small__0rf0J') and text()='Онлайн оплата картой']",
                )
            )
        )
        online_payment_button.click()
        print("Кнопка 'Онлайн оплата картой' нажата.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Клик на кнопку "Оформить заказ"
    next_btn_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Оформить заказ']"))
    )

    next_btn_3.click()
    print("Кнопка Оформить заказ нажата.")

    time.sleep(7)

    # Ввод номера машины
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input.Input_input__BbM8T.styles_input__3lJwv")
        )
    )

    try:
        ActionChains(driver).move_to_element(input_field).click().perform()
        print("Поле ввода найдено и на него выполнен клик.")

        input_field.send_keys("717wvw17")
        time.sleep(1)
        print(
            "Текст '717wvw17' успешно введен."
        )  # Укажите номер, который хотите ввести

    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    # Клик на кнопку "Подключить сервис"
    try:
        connect_service_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[text()='Подключить сервис']",
                )
            )
        )
        connect_service_btn.click()
        print("Кнопка - Подключить сервис нажата")

    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(3)

    # Клик на кнопку "Оплата онлайн"
    try:
        oplata_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(@class, 'Button_button__a61EI') and contains(@class, 'Button_primary__P0bZq') and contains(@class, 'Button_medium__lxzcc') and contains(@class, 'OrderStatus_btn__Ifia1')]",
                )
            )
        )
        oplata_button.click()
        print(
            "Кнопка с классом 'Button_button__a61EI Button_primary__P0bZq Button_medium__lxzcc OrderStatus_btn__Ifia1' успешно нажата."
        )
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        pan_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pan"))
        )
        pan_input.click()
        pan_input.send_keys("4111 1111 1111 1111")
        print("Номер карты успешно введен в поле с id='pan'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        month_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        month_input.click()
        month_input.send_keys("12")
        print("Значение '12' успешно введено в поле с id='month'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        year_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "year"))
        )
        year_input.click()
        year_input.send_keys("30")
        print("Значение '30' успешно введено в поле с id='year'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        cvv_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cvv"))
        )
        cvv_input.click()
        cvv_input.send_keys("123")
        print("Значение '123' успешно введено в поле с id='cvv'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        holder_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "holder"))
        )
        holder_input.click()
        holder_input.send_keys("Test test")
        print("Текст 'Test test' успешно введен в поле с id='holder'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        telephone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "telephone"))
        )
        telephone_input.click()
        telephone_input.send_keys("77075007554")
        print("Номер телефона успешно введен в поле с id='telephone'.")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.click()
        email_input.send_keys("eldar.koziyev@fdrive.kz")
        print("email введен")
    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Оплатить')]")
            )
        )
        driver.execute_script("arguments[0].click();", button)
        print("Кнопка нажата через JavaScript.")
    except Exception as e:
        print(f"Ошибка: не удалось кликнуть по кнопке через JavaScript: {e}")
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

        raise SystemExit("Тест завершен из-за ошибки: кнопка Оплатить не найдена")


    time.sleep(5)
    # Сохраняет номер заказа
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Заказ')]")

        for element in elements:
            text = element.text
            match = re.search(r"Заказ\s*(\d+)", text)
            if match:
                order_number = match.group(1)
                print(f"Найден номер заказа: {order_number}")
                break
        else:
            print("Номер заказа не найден.")

    except Exception as e:
        # Делаем скриншот ошибки
        timestamp = int(time.time())  # для уникальности имени файла
        screenshot_path = f"screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        
        error_message = f"Произошла ошибка при нажатии на кнопку: {e}"
        print(error_message)
        
        # Отправляем ошибку и скриншот в Telegram
        send_error_to_telegram(error_message, screenshot_path)

    time.sleep(3)

    # ///////////////////////////////////////////////////////////////////////

finally:
    time.sleep(5)
    driver.quit()
