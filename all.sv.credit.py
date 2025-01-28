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

# Настройка драйвера
options = Options()
#options.add_argument("--headless")
#options.add_argument("--window-size=1920x1080")
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
        select_whell_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[text()='Подобрать шины']",
                )
            )
        )
        select_whell_button.click()
        print("Кнопка - Подобрать шины нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 2000);")
    time.sleep(1)

    try:
        # Ожидание появления элемента на странице
        link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@href='/tyres/almaty/page2']")
            )
        )

        # Пролистывание до элемента
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            link_element,
        )

        # Нажатие на элемент
        link_element.click()
        print("Ссылка '/tyres/almaty/page2' успешно нажата.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    driver.execute_script("window.scrollBy(0, 600);")
    time.sleep(1)

    # Клик на кнопку "Добавить в корзину"
    time.sleep(5)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Ожидаем появления кнопок
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
        print("Ошибка: не удалось кликнуть по кнопке после нескольких попыток.")

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

    try:
        add_drive_plus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div[3]/button",
                )
            )
        )

        driver.execute_script("arguments[0].click();", add_drive_plus)
        print("Кнопка Добавить услгу - Drive+ успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку 'Drive+': {e}")

    time.sleep(2)

    try:
        add_wheel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[3]/button",
                )
            )
        )

        driver.execute_script("arguments[0].click();", add_wheel)
        print("Кнопка Добавить услгу - Шиномонтаж успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку 'Шиномонтаж': {e}")

    time.sleep(2)

    try:
        tire_storage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[3]/button",
                )
            )
        )

        driver.execute_script("arguments[0].click();", tire_storage)
        print("Кнопка Добавить услгу - Хранение шин успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку 'Хранение шин': {e}")

    time.sleep(3)
    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(1)
    # Клик на кнопку "Переход к оформению"
    try:
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Перейти к оформлению']"))
        )

        checkout_button.click()
        print("Нажата кнопка 'Перейти к оформлению'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Ввод телефона
    try:
        phone_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "phoneNumber"))
        )

        phone_input.click()

        phone_input.send_keys("7075007554")
        print("Номер телефона введен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Ввод имени
    try:
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "userName"))
        )

        name_input.click()

        name_input.send_keys("Eldar")
        print("Имя пользователя введено.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(2)

    # Клик на кнопку "Продолжить"
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Продолжить']"))
        )

        next_btn.click()
        print("Кнопка продолжить нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(3)
    
    try:
        # Выбираем способ доставки - Самовывоз
        shipment_methods = driver.find_elements(By.XPATH, "//input[@name='shipmentServiceId']")

        for method in shipment_methods:
            if method.get_attribute('value') == 'ecar_selfservice':
                print('method')
                print(method)
                method.click()
                print("Кнопка 'Самовывоз' нажата.")
                break
    except Exception as e:
        print(f"Ошибка {e}")
    
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(3)

    try:
        map_container = driver.find_element(By.XPATH, "//*[@id='yandexMap']")
        
        placemark = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='yandexMap']/ymaps/ymaps/ymaps/ymaps[5]/ymaps[3]"))
        )
        
        actions = ActionChains(driver)
        
        actions.move_to_element(placemark).click().perform()
        print("Элемент найден, мышь наведена, и клик выполнен.")
        
    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(5) 
        
    try:
        # Взаимодействие с кнопкой "Выбрать"
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Выбрать']"))
            )
            button.click()
    except Exception as e:
            print(f"Ошибка: {e}")

    time.sleep(3)

    # Выбор способа оплаты
    try:
        online_payment_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(@class, 'Subtitle_root__LPeeH') and contains(@class, 'Subtitle_small__0rf0J') and text()='Кредит/рассрочка']",
                )
            )
        )
        online_payment_button.click()
        print("Кнопка 'Кредит/рассрочка' нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Клик на кнопку "Оформить заказ"
    next_btn_3 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Оформить заказ']"))
    )

    next_btn_3.click()
    print("Кнопка Оформить заказ нажата.")

    time.sleep(10)

    try:
        IIN_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Input_input__BbM8T"))
        )
        #IIN_btn.click()
        IIN_btn.send_keys("930513402104")
        print("ИИН введен")
    except Exception as e:
        print(f"Произошла ошибка: {e}")  

    time.sleep(5)

    try:
        select_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,"//*[text()='Подтвердить по SMS']"))
        )      
        select_btn.click()
        print("Кнопка Подтверлить по СМС - нажата")
    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(3)

    try:
        # Найти кнопку по классу optCode
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Input_hasRightIcon__8lOPx"))
        )
        # Выполнить клик через JavaScript
        driver.execute_script("arguments[0].click();", button)
        print("Кнопка с классом 'optCode' нажата.")
        
    
        input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "Input_hasRightIcon__8lOPx"))
            )
        input_field.clear()
        input_field.click()
        for char in "111111":
            input_field.send_keys(char)
            time.sleep(0.1)  # Имитация задержки между вводом символов
            print("Текст '111111' введен символ за символом.")
    except Exception as e:
            print(f"Ошибка: {e}")

    time.sleep(3)

    try:
        confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Подтвердить']"))
        )   
        confirm_button.click()
        print("Кнопка 'Подтвердить' нажата.")
    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(30)

    try:
        offers_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "BankItem_offersRow___eYw6"))
        )
        print("Элемент с классом 'BankItem_offersRow___eYw6' найден.")

        button_6 = offers_row.find_element(By.XPATH, '//*[@id="main-content"]/div/section/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/label/input')
        button_6.click()
        print("Кнопка нажата.")
    except Exception as e:
        print(f"Ошибка при попытке найти или нажать кнопку: {e}")
        assert False, f"Тест остановлен из-за ошибки: {e}"

    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(2)

    try:
        confirm_credit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Выбрать предложение']"))
        )
        confirm_credit_btn.click()
        print("Кнопка Выбрать предложение нажата")
    except Exception as e:
        print(f"ошибка в нажатии копки 'Выбрать предложение'")
    
    time.sleep(5)    
finally:
    driver.quit()

