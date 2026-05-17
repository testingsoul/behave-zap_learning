from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from behave_zap import PageObject, InputText, Button


class MainPagePageObject(PageObject):
    def init_page_elements(self):
        self.close_welcome_banner = Button(By.XPATH, "//button[@aria-label='Close Welcome Banner']")
        self.cookie_consent = Button(By.XPATH, "//a[@aria-label='dismiss cookie message']")
        self.side_menu = Button(By.XPATH, "//button[@aria-label='Open Sidenav']")
        self.customer_feedback = Button(By.XPATH, "//a[@aria-label='Go to contact us page']")
        self.search_button = Button(By.ID, "searchQuery")
        self.search = InputText(By.CSS_SELECTOR, "#searchQuery input")
        self.home = Button(By.ID, "homeButton")
        self.add_to_cart = Button(By.XPATH, "//button[@aria-label='Add to Basket']")
        self.basket = Button(By.XPATH, "//button[@routerlink='/basket']")

    def open(self):
        """ Open login url in browser

        :returns: this page object instance
        """
        self.driver.get('{}'.format(self.config.get('Test', 'url')))
        self.close_welcome_banner.click()
        self.cookie_consent.click()
        return self


    def login(self):
        """ Fill login form and submit it

        :param user: dict with username and password values
        :returns: secure area page object instance
        """
        self.account_menu.click()
        self.login_link.click()
        self.wait_until_loaded()
        user = {
            'username': self.config.get('Test', 'username'),
            'password': self.config.get('Test', 'password')
        }
        self.username.text = user['username']
        self.password.text = user['password']
        self.submit.click()


    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.username.wait_until_visible()
        return self

    def add_first_visible_product_to_cart(self):
        """Click an add-to-basket button from visible product results using resilient locators."""
        button_locators = [
            (By.XPATH, "(//button[@aria-label='Add to Basket' and not(@disabled)])[1]"),
            (By.XPATH, "(//mat-card//button[.//span[contains(normalize-space(.), 'Add to Basket')]])[1]"),
        ]

        for by, value in button_locators:
            try:
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((by, value))
                )
                try:
                    button.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", button)
                return
            except TimeoutException:
                continue

        raise TimeoutException("No visible and clickable Add to Basket button found")
