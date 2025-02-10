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

# Настройка драйвера
options = Options()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(), options=options)

try:
    driver.get("https://front-qa.ecar.kz/")
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

   # Указываем папку для сохранения
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)  # Создаем папку, если ее еще нет

    # Путь для сохранения скриншота
    screenshot_path = os.path.join(screenshot_dir, "screenshot.png")

    # Сохраняем скриншот
    driver.save_screenshot(screenshot_path)
    print(f"Скриншот сохранен в {screenshot_path}")     

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
        drive_plus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[text()='Гарантия ']",
                )
            )
        )
        print("Услуга Drive+ - найдена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        tire_service = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[text()='Шиномонтаж']",
                )
            )
        )
        print("Услуга Шиномонтаж - найдена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        tire_storage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[text()='Хранение шин']",
                )
            )
        )
        print("Услуга Хранение шин - найдена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(3)

    try:
        plus_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div/button[2]",
                )
            )
        )

        driver.execute_script("arguments[0].click();", plus_button)
        print("Кнопка '+' успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку '+': {e}")

    time.sleep(3)

    try:
        minus_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div/button[1]",
                )
            )
        )
        driver.execute_script("arguments[0].click();", minus_button)
        print("Кнопка '-' успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку '+': {e}")

    time.sleep(3)

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
        print(f"Ошибка при нажатии на кнопку '+': {e}")

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
        print(f"Ошибка при нажатии на кнопку '+': {e}")

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
        print(f"Ошибка при нажатии на кнопку '+': {e}")

    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(1)

    try:
        remove_service = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/button",
                )
            )
        )

        driver.execute_script("arguments[0].click();", remove_service)
        print("Кнопка - убрать услугу успешно нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку '+': {e}")

    time.sleep(2)

    try:
        delet_basket = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='main-content']/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/button",
                )
            )
        )

        driver.execute_script("arguments[0].click();", delet_basket)
        print("Кнопка - удалить с корзины нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии на кнопку '+': {e}")

# Переход в админку для отмены заказа
    try:
        driver.get("https://old-qa.ecar.kz/account/logon?returnUrl=%2fcabinet")  # Переход к старой версии админки
        driver.maximize_window()

        # Ввод логина
        admin_username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        admin_username_input.send_keys("ramash.yerkezhan1")
        print("Логин администратора введен.")

        # Ввод пароля
        admin_password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        admin_password_input.send_keys("Alm123456")
        print("Пароль администратора введен.")

        # Клик на кнопку "Войти"
        admin_login_submit = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Войти')]"))
        )
        admin_login_submit.click()
        print("Кнопка 'Войти' нажата.")

        # Поиск созданного заказа для отмены
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "idOrCode"))
        )
        search_input = driver.find_element(By.NAME, "idOrCode")
        search_input.send_keys(order_number)
        search_input.send_keys(Keys.RETURN)
        print(f"Заказ {order_number} найден.")
        
        # Скроллим вниз до нужного элемента
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//select[@id='orderCancelReason']"))
            ).click()
            print("Элемент 'orderCancelReason' доступен и кликнут.")
        except Exception as e:
            print(f"Ошибка при клике на 'orderCancelReason': {e}")

        # Прокручиваем страницу вниз
        try:
            driver.execute_script("arguments[0].scrollIntoView();", cancel_reason_select)
            print("Прокрутка страницы вниз выполнена.")
        except Exception as e:
            print(f"Ошибка при прокрутке страницы вниз: {e}")

        # Выбираем статус "Отменен"
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Отменен']"))
            ).click()
            print("Статус 'Отменен' выбран.")
        except Exception as e:
            print(f"Ошибка при выборе статуса 'Отменен': {e}")

        # Даем немного времени для полной загрузки страницы
        time.sleep(3)

        # Далее поиск элемента
        try:
            cancel_reason_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "orderCancelReason"))
            )
            cancel_reason_select.click()
            print("Элемент 'orderCancelReason' найден и кликнут.")
            time.sleep(1)  # Даем время для появления элементов
            cancel_reason_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//option[@value='301']"))  # Выбор "Тестовый заказ"
            )
            cancel_reason_option.click()
            print("Причина отмены введена.")
        except Exception as e:
            print(f"Ошибка при выборе причины отмены: {e}")

        # Клик на кнопку "Отменить заказ"
        try:
            cancel_order_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @class='btn btn-primary' and contains(text(), 'Отправить')]"))
            )
            cancel_order_button.click()
            print(f"Заказ {order_number} отменен.")
        except Exception as e:
            print(f"Ошибка при клике на 'Отменить заказ': {e}")

        # Проверка статуса "Отменен"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Отменен']"))
            )
            print(f"Статус заказа {order_number} - 'Отменен'")
        except TimeoutException:
            print(f"Статус заказа {order_number} не изменился.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

finally:
    time.sleep(5)
    driver.quit()
