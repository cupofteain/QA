import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
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

def log_message(message):
    log_field.insert(tk.END, message + "\n")
    log_field.see(tk.END)  # Автопрокрутка вниз
    window.update()

def run_test():
    driver = webdriver.Chrome()
        
    try:
        driver.get("https://front-qa.ecar.kz/")
        time.sleep(3)
        driver.maximize_window()
        log_message("🌐 Открыта страница для теста ✔️")
    except Exception as e:
        log_message(f"❌ Ошибка: {e}")

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
        log_message("Кнопка нажата ✔️")
    except Exception as e:
        print(f"Произошла ошибка: {e}")




    finally:
        time.sleep(3)
        driver.quit()
        log_message("🛑 Браузер закрыт.")

# Создание окна Tkinter
window = tk.Tk()
window.title("Логи автотеста")
window.geometry("500x400")

# Поле для логов
log_field = tk.Text(window, wrap="word", height=20, width=60)
log_field.pack(padx=10, pady=10)

# Кнопка для запуска теста
run_button = tk.Button(window, text="Запустить тест", command=run_test)
run_button.pack(pady=5)

# Запуск интерфейса
window.mainloop()
