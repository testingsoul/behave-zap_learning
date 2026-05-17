from selenium.webdriver.common.by import By

from behave_zap import PageObject, InputText, Button


class BasketPageObject(PageObject):
    def init_page_elements(self):
        self.delete_item = Button(By.XPATH, "//mat-row[1]/mat-cell[5]//button")
        self.sum_item = Button(By.XPATH, "//mat-row[1]/mat-cell[3]//button[2]")



    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.delete_item.wait_until_visible()
        return self