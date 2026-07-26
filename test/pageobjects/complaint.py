import os

from selenium.webdriver.common.by import By

from behave_zap import PageObject, InputText, Button, Text


class ComplaintPageObject(PageObject):
    def init_page_elements(self):
        self.message = InputText(By.ID, "complaintMessage")
        self.invoice = InputText(By.ID, "file")
        self.submit = Button(By.ID, "submitButton")
        self.success_message = Text(
            By.XPATH,
            "//p[contains(@class,'confirmation') and contains(.,'Customer support will get in touch')]",
        )

    def upload_invoice(self, filename="invoice.pdf"):
        """ Attach an invoice file to the complaint form.

        :param filename: file located in test/fixtures to upload
        :returns: this page object instance
        """
        fixtures_dir = os.path.join(os.path.dirname(__file__), "..", "fixtures")
        invoice_path = os.path.abspath(os.path.join(fixtures_dir, filename))
        self.invoice.find().send_keys(invoice_path)
        return self

    def wait_until_loaded(self):
        """ Wait until complaint page is loaded

        :returns: this page object instance
        """
        self.message.wait_until_visible()
        return self
