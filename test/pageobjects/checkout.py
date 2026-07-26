from selenium.webdriver.common.by import By

from behave_zap import PageObject, InputText, Button


class CheckoutPageObject(PageObject):
    def init_page_elements(self):
        self.select_address = Button(By.XPATH, "//mat-row[last()]//mat-radio-button")
        self.delivery_speed = Button(By.XPATH, "//mat-row[1]//mat-radio-button")
        self.payment_card = Button(By.XPATH, "//mat-row[1]//mat-radio-button")
        self.proceed_button = Button(By.XPATH, "//button[@aria-label='Proceed to payment selection']")
        self.delivery_button = Button(By.XPATH, "//button[@aria-label='Proceed to delivery method selection']")
        self.review_button = Button(By.XPATH, "//button[@aria-label='Proceed to review']")
        self.checkout_button = Button(By.ID, "checkoutButton")
        
        ## Add new address
        self.add_address_panel = Button(By.XPATH, "//button[@aria-label='Add a new address']")
        self.address_country = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Country']]//input")
        self.address_name = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Name']]//input")
        self.address_mobile_number = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Mobile Number']]//input")
        self.address_zip_code = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='ZIP Code']]//input")
        self.address_address = InputText(By.ID, "address")
        self.address_city = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='City']]//input")
        self.address_state = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='State']]//input")
        self.address_submit = Button(By.ID, "submitButton")

        ## Add new card
        self.add_card_panel = Button(By.XPATH, "//mat-panel-title[normalize-space(.)='Add new card']")
        self.card_name = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Name']]//input")
        self.card_number = InputText(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Card Number']]//input")
        self.card_expiry_month = Button(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Expiry Month']]//select")
        self.card_expiry_year = Button(By.XPATH, "//mat-form-field[.//mat-label[normalize-space(.)='Expiry Year']]//select")
        self.card_submit = Button(By.ID, "submitButton")


    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.proceed_button.wait_until_visible()
        return self