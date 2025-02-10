from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        #ERROR: Caught exception [unknown command []]
        driver.get("https://front-qa.ecar.kz/")
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/div[2]/div/div/div/div/div[2]/div[3]/div/button").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/div/a/button").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/div/a/button").click()
        driver.find_element_by_xpath(u"//img[@alt='Гипермаркет шин ecar.kz']").click()
        driver.find_element_by_xpath("//section[@id='mainSection']/header/div").click()
        driver.find_element_by_xpath(u"//img[@alt='Гипермаркет шин ecar.kz']").click()
        driver.get(self.base_url + "chrome://newtab/")
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Алматы?'])[1]/following::*[name()='svg'][1]").click()
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Подобрать шины'])[1]/following::*[name()='svg'][1]").click()
        driver.find_element_by_link_text("2").click()
        driver.get("https://front-qa.ecar.kz/tyres/almaty/page2")
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Кешбэк до 12%'])[5]/following::*[name()='svg'][3]").click()
        driver.find_element_by_xpath("//section[@id='mainSection']/header/div/div[3]/a[2]/button").click()
        driver.get("https://front-qa.ecar.kz/cart")
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/div[2]/div[2]/div[2]/div/div[2]/div/button/span").click()
        driver.get("https://front-qa.ecar.kz/checkout")
        driver.find_element_by_name("phoneNumber").click()
        driver.find_element_by_name("phoneNumber").clear()
        driver.find_element_by_name("phoneNumber").send_keys("+7 747 147 2003")
        driver.find_element_by_name("userName").click()
        driver.find_element_by_name("userName").clear()
        driver.find_element_by_name("userName").send_keys(u"Удзумаки Наруто")
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Продолжить'])[1]/following::*[name()='svg'][1]").click()
        driver.find_element_by_name("shipmentAddress").click()
        driver.find_element_by_name("shipmentAddress").clear()
        driver.find_element_by_name("shipmentAddress").send_keys(u"Абая 14")
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/main/div/div/div[2]/form/div[3]/fieldset/label[2]/div").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/main/div/div/div[2]/form/div[4]/fieldset[2]/label[2]/div").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/div/main/div/div/div[2]/form/button/span").click()
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Оформить заказ'])[1]/following::*[name()='svg'][1]").click()
        driver.find_element_by_name("auto_number").click()
        driver.find_element_by_name("auto_number").clear()
        driver.find_element_by_name("auto_number").send_keys("012AAA01")
        driver.find_element_by_xpath("//div[@id=':r4h:']/div/div/form/button/span").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/section/div[2]/div[2]/div[2]/div/h5/span").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/section/div[2]/div[2]/div[2]/div/h5/span").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/section/div[2]/div[2]/div[2]/div/h5/span").click()
        driver.find_element_by_xpath("//section[@id='main-content']/div/section/div[2]/div[2]/div[2]/div/h5/span").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
