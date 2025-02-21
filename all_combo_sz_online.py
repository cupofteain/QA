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
from selenium.common.exceptions import ElementClickInterceptedException
import time
import re
import random

# Настройка драйвера
options = Options()
#options.add_argument("--headless")
#options.add_argument("--window-size=1920x1080")
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

    # Скроллим немного вниз, чтобы кнопка была в зоне видимости
    driver.execute_script("window.scrollBy(0, 100);")
    time.sleep(1)

    # Нажатие на кнопку "Подобрать шины"
    try:
        select_tyres_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[text()='Подобрать шины']")
            )
        )
        select_tyres_button.click()
        print("Кнопка - Подобрать шины нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(3)

    # Переход на вторую страницу
    try:
        while True:
            try:
                # Пытаемся найти элемент и кликнуть на него
                next_page_link = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[@href="/tyres/almaty/page2"]'))
                )
                driver.execute_script("arguments[0].click();", next_page_link)
                print("Перешли на вторую страницу шин.")
                break
            except TimeoutException:
                # Если элемент не найден, скроллим страницу вниз
                driver.execute_script("window.scrollBy(0, 100);")
                print("Скроллим страницу вниз...")
            except ElementClickInterceptedException:
                print("Элемент не кликабелен, скроллим страницу.")
                driver.execute_script("window.scrollBy(0, 100);")
    except Exception as e:
        print(f"Ошибка при переходе на вторую страницу: {e}")

    time.sleep(3)

    # Клик на случайную кнопку "Добавить в корзину"
    max_retries = 3
    for attempt in range(max_retries):
        try:
            product_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductCardAlternative_addCart__CCEoW"))
            )

            if product_buttons:
                random_button = random.choice(product_buttons)

                try:
                    random_button.click()
                    print("Случайная кнопка 'Добавить в корзину' нажата.")
                    break
                except Exception as e:
                    driver.execute_script("arguments[0].click();", random_button)
                    print("Случайная кнопка 'Добавить в корзину' нажата с помощью execute_script.")
                    break
            else:
                print("Ошибка: кнопки 'Добавить в корзину' не найдены.")
                break

        except StaleElementReferenceException:
            print(f"Попытка {attempt + 1} из {max_retries}: элемент устарел, пробуем снова...")
            driver.execute_script("window.scrollBy(0, 100);")
            print(f"Скроллинг вниз перед попыткой {attempt + 1}...")
            time.sleep(2)
    else:
        print("Ошибка: не удалось кликнуть по кнопке после нескольких попыток.")
        time.sleep(2)

    # Возвращаемся назад
    try:
        driver.back()
        time.sleep(2)
        driver.back()
        time.sleep(3)
        print("Вернулись назад.")
    except Exception as e:
        print(f"Ошибка при возврате назад: {e}")

    # Скроллим немного вниз, чтобы кнопка была в зоне видимости
    driver.execute_script("window.scrollBy(0, 100);")
    time.sleep(1)

    # Нажимаем на кнопку "Подобрать диски"
    try:
        select_wheels_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'Button_button__a61EI')]/span[text()='Подобрать диски']",
                )
            )
        )
        select_wheels_button.click()
        print("Кнопка - Подобрать диски нажата.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(3)

    # Клик на случайную кнопку "Добавить в корзину" для дисков
    for attempt in range(max_retries):
        try:
            product_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ProductCardAlternative_addCart__CCEoW"))
            )
            if product_buttons:
                random_button = random.choice(product_buttons)
                try:
                    random_button.click()
                    print("Случайная кнопка 'Добавить в корзину' (диски) нажата.")
                    break
                except Exception as e:
                    driver.execute_script("arguments[0].click();", random_button)
                    print("Случайная кнопка 'Добавить в корзину' (диски) нажата с помощью execute_script.")
                    break
            else:
                print("Ошибка: кнопки 'Добавить в корзину' (диски) не найдены.")
                break
        except StaleElementReferenceException:
            print(f"Попытка {attempt + 1} из {max_retries}: элемент устарел, пробуем снова...")
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(2)
    else:
        print("Ошибка: не удалось кликнуть по кнопке после нескольких попыток.")

    time.sleep(2)

    # Нажимаем на кнопку "Каталог"
    try:
        catalog_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button_button__a61EI')]//span[text()='Каталог']"))
        )

        actions = ActionChains(driver)
        actions.move_to_element(catalog_button).perform()
        catalog_button.click()
        print("Кнопка 'Каталог' нажата.")
    except Exception as e:
        print(f"Ошибка при нажатии кнопки 'Каталог': {e}")

    time.sleep(2)

    # Выбираем случайный раздел
    categories = ["Жидкости", "Химия", "Аксессуары", "Запчасти"]

    # Выбираем случайную категорию
    selected_category = random.choice(categories)
    print(f"Выбрана категория: {selected_category}")

    try:
        # Ищем нужный элемент по тексту
        category_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(@class, 'Catalog_itemLabel__V9TPw') and text()='{selected_category}']")
            )
        )
        
        # Скроллим к элементу
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_element)
        time.sleep(1)  # Небольшая задержка, чтобы скролл применился
        
        # Кликаем по элементу
        category_element.click()
        print(f"Кликнуто по категории: {selected_category}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
        # Получаем все кнопки "Добавить в корзину"
    add_to_cart_buttons = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'Button_button__a61EI') and contains(@class, 'ProductCardCategory_button__O5_fb')]"))
    )

    # Выбираем случайную кнопку
    random_button = random.choice(add_to_cart_buttons)
    
    # Прокручиваем страницу до выбранной кнопки
    ActionChains(driver).move_to_element(random_button).perform()

    # Явно ждем, пока кнопка станет кликабельной
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(random_button)
    )

    # Кликаем по выбранной кнопке
    random_button.click()

    print("Случайная кнопка 'Добавить в корзину' нажата.")
    
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
        
    # Функция для добавления услуги по data-test-id
    def add_service(service_id, service_name):
        try:
            # Ожидаем появления карточки услуги
            service_card = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//div[@data-test-id='{service_id}']"))
            )

            # Ищем кнопку "Добавить услугу" внутри карточки
            add_button = service_card.find_element(By.XPATH, ".//button[span[text()='Добавить услугу']]")
            
            # Кликаем по кнопке
            add_button.click()
            print(f"Услуга '{service_name}' добавлена.")

        except Exception as e:
            print(f"Ошибка при добавлении услуги '{service_name}': {e}")

    # Добавление всех услуг
    services = {
        "service-card-shinomontazh": "Шиномонтаж",
        "service-card-service-cart-storage": "Хранение шин",
        "service-card-drivePlus": "Гарантия Drive+"
    }

    for service_id, service_name in services.items():
        add_service(service_id, service_name)
    
    # Клик на кнопку "Переход к оформлению"
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

        phone_input.send_keys("7471472003")
        print("Номер телефона введен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Ввод имени
    try:
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "userName"))
        )

        name_input.click()

        name_input.send_keys("yerkezhan")
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

    # Выбор способа доставки
    try:
        client_blue_zone = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//input[@name='shipmentServiceId' and @value='ecar_courier_zone2']",
                )
            )
        )
        client_blue_zone.click()
        print("Кнопка - Выбора доставки нажата")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

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
        print(f"Произошла ошибка: {e}")

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
        print(f"Произошла ошибка: {e}")

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
        print(f"Произошла ошибка: {e}")

    # Клик на кнопку "Продолжить"
    next_btn_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Продолжить']"))
    )

    next_btn_2.click()
    print("Кнопка продолжить нажата.")
    time.sleep(2)

    # Выбор способа оплаты
    try:
        online_payment_label = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[.//span[contains(text(), 'Онлайн оплата картой')]]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", online_payment_label)
        online_payment_label.click()
        print("Клик выполнен после скролла.")
    except Exception as e:
        print(f"Ошибка: {e}")


    try:
    # Клик на кнопку "Оформить заказ"
        next_btn_3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Оформить заказ']"))
        )

        next_btn_3.click()
        print("Кнопка Оформить заказ нажата.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
    time.sleep(3)

    # Ввод номера машины
    try:
        input_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.Input_input__BbM8T.styles_input__3lJwv"))
        )
        ActionChains(driver).move_to_element(input_field).click().perform()
        print("Поле ввода найдено и на него выполнен клик.")

        input_field.send_keys("244yer02")
        time.sleep(1)
        print("Текст '244yer02' успешно введен.")

        # После ввода номера пробуем нажать "Подключить сервис"
        try:
            connect_service_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Подключить сервис']"))
            )
            connect_service_btn.click()
            print("Кнопка 'Подключить сервис' нажата.")
            time.sleep(3)  # Ждём возможное появление окна

        except TimeoutException:
            print("Кнопка 'Подключить сервис' не появилась, пропускаем этот шаг.")

    except TimeoutException:
        print("Поле ввода номера машины не найдено, пропускаем шаг.")
        
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
        print(f"Произошла ошибка: {e}")

    try:
        pan_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pan"))
        )
        pan_input.click()
        pan_input.send_keys("4111 1111 1111 1111")
        print("Номер карты успешно введен в поле с id='pan'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        month_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        month_input.click()
        month_input.send_keys("12")
        print("Значение '12' успешно введено в поле с id='month'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        year_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "year"))
        )
        year_input.click()
        year_input.send_keys("30")
        print("Значение '30' успешно введено в поле с id='year'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        cvv_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cvv"))
        )
        cvv_input.click()
        cvv_input.send_keys("123")
        print("Значение '123' успешно введено в поле с id='cvv'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        holder_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "holder"))
        )
        holder_input.click()
        holder_input.send_keys("Test test")
        print("Текст 'Test test' успешно введен в поле с id='holder'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        telephone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "telephone"))
        )
        telephone_input.click()
        telephone_input.send_keys("77075007554")
        print("Номер телефона успешно введен в поле с id='telephone'.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.click()
        email_input.send_keys("yerlezhan@fdrive.kz")
        print("email введен")
    except Exception as e:
        print(f"email не удалось ввести: {e}")

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
        print(f"Произошла ошибка: {e}")
    time.sleep(3)

        # ///////////////////////////////////////////////////////////////////////
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
            cancel_reason_select = driver.find_element((By.XPATH, '//*[@id="order-info-main-info"]/div[1]/div[4]/div[2]/div[9]/div[4]/label/span'))
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
