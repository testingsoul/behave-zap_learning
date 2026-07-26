import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from behave_zap import PageObject, InputText, Button


class LoginPageObject(PageObject):
    def init_page_elements(self):
        self.account_menu = Button(By.ID, "navbarAccount")
        self.login_link = Button(By.ID, "navbarLoginButton")
        self.username = InputText(By.ID, "email")
        self.password = InputText(By.ID, "password")
        self.submit = Button(By.ID, "loginButton")
        self.error_message = Button(By.XPATH, "//*[contains(text(),'Invalid email or password.')]")
        self.close_welcome_banner = Button(By.XPATH, "//button[@aria-label='Close Welcome Banner']")
        self.cookie_consent = Button(By.XPATH, "//a[@aria-label='dismiss cookie message']")

        self.new_customer = Button(By.XPATH, "//div[@id='newCustomerLink']/a")
        self.new_username = InputText(By.ID, "emailControl")
        self.new_password = InputText(By.ID, "passwordControl")
        self.rep_password = InputText(By.ID, "repeatPasswordControl")
        self.security_question = Button(By.CSS_SELECTOR, "[data-test='security-answer-select'], mat-select[formcontrolname='securityQuestion']")
        self.security_question_sel = Button(By.XPATH, "//mat-option//span[contains(normalize-space(.), 'Your eldest sibling')]")
        self.security_answer = InputText(By.ID, "securityAnswerControl")
        self.register = Button(By.ID, "registerButton")


    def open(self):
        """ Open login url in browser

        :returns: this page object instance
        """
        self.driver.get('{}'.format(self.config.get('Test', 'url')))
        try: 
            self.close_welcome_banner.wait_until_clickable(timeout=1)
            self.close_welcome_banner.click()
            self.cookie_consent.click()
        except Exception as e:
            print(f"Error closing welcome banner or cookie consent: {e}")
        return self


    def login(self, username=None, password=None):
        """ Fill login form and submit it

        :param user: dict with username and password values
        :returns: secure area page object instance
        """
        self.account_menu.click()
        try:
            self.login_link.wait_until_clickable(timeout=0.5)
            self.login_link.click()
        except TimeoutException:
            print("Login link not clickable after 0.5s. Assuming user is already logged in.")
            self.open()  # Refresh the page to ensure we're in a consistent state
            return
        self.wait_until_loaded()
        if username or password:
            user = {
                'username': username,
                'password': password
            }
        else:
            user = {
                'username': self.config.get('Test', 'username'),
                'password': self.config.get('Test', 'password')
            }
        self.username.clear()
        if username != "":
            self.username.text = user['username']
        self.password.clear()
        if password != "":
            self.password.text = user['password']
        if username != "" and password != "":
            self.submit.click()

    def create_user(self, username=None, password=None):
        """ Fill registration form and submit it

        :param username: username to register; falls back to config when empty
        :param password: password to register; falls back to config when empty
        :returns: secure area page object instance
        """
        self.account_menu.click()
        self.login_link.click()


        self.wait_until_loaded()
        time.sleep(2)
        self.new_customer.click()
        if username or password:
            user = {
                'username': username,
                'password': password
            }
        else:
            user = {
                'username': self.config.get('Test', 'username'),
                'password': self.config.get('Test', 'password')
            }
        self.new_username.text = user['username']
        self.new_password.text = user['password']
        self.rep_password.text = user['password']
        self._select_security_question()
        self.security_answer.text = "Any answer"
        self.register.click()

    def _select_security_question(self):
        """Open security question dropdown and pick a valid option using stable fallbacks."""
        dropdown_locators = [
            (By.CSS_SELECTOR, "mat-select[formcontrolname='securityQuestion']"),
            (By.CSS_SELECTOR, "mat-select[name='securityQuestion']"),
            (By.XPATH, "//mat-label[contains(normalize-space(.), 'Security Question')]/ancestor::mat-form-field//mat-select"),
        ]
        option_locators = [
            (By.XPATH, "//mat-option//span[contains(normalize-space(.), 'Your eldest sibling')]"),
            (By.XPATH, "//mat-option[not(@disabled)][1]"),
        ]

        dropdown = None
        for by, value in dropdown_locators:
            try:
                dropdown = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, value))
                )
                break
            except TimeoutException:
                continue

        if dropdown is None:
            raise TimeoutException("Security question dropdown not found/clickable")

        try:
            dropdown.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", dropdown)

        for by, value in option_locators:
            try:
                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((by, value))
                )
                try:
                    option.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", option)
                return
            except TimeoutException:
                continue

        raise TimeoutException("No selectable security question option found")

    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.username.wait_until_visible()
        return self
