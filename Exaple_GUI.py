import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Логи автотеста")
        self.setGeometry(100, 100, 500, 400)

        # Set up layout
        self.layout = QVBoxLayout()

        # Log field
        self.log_field = QTextEdit(self)
        self.log_field.setReadOnly(True)
        self.layout.addWidget(self.log_field)

        # Run test button
        self.run_button = QPushButton("Запустить тест", self)
        self.run_button.clicked.connect(self.run_test)
        self.layout.addWidget(self.run_button)

        # Set layout for the window
        self.setLayout(self.layout)

    def log_message(self, message):
        self.log_field.append(message)

    def run_test(self):
        driver = webdriver.Chrome()
        
        try:
            driver.get("https://front-qa.ecar.kz/")
            time.sleep(3)
            driver.maximize_window()
            self.log_message("🌐 Открыта страница для теста ✔️")
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")

        try:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'CitySelectModal_actionButton')]")
                )
            )
            confirm_button.click()
            self.log_message("Кнопка нажата ✔️")
        except TimeoutException:
            self.log_message("❌ Кнопка не была найдена или не стала кликабельной в течение 10 секунд.")
        except Exception as e:
            self.log_message(f"❌ Произошла ошибка: {e}")

        finally:
            time.sleep(3)
            driver.quit()
            self.log_message("🛑 Браузер закрыт.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
