from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from behave_zap import PageObject, InputText, Button, Text


class CustomerFeedbackPageObject(PageObject):
    def init_page_elements(self):
        self.comment = InputText(By.XPATH, "//textarea[@aria-label='Field for entering the comment or the feedback']")
        self.rating = Button(By.XPATH, "//div[@style='transform: translateX(26.5px);']")
        self.captcha_to_eval = Text(By.ID, "captcha")
        self.captcha = InputText(By.ID, "captchaControl")
        self.submit = Button(By.ID, "submitButton")
        self.success_message = Text(By.XPATH, "//simple-snack-bar//*[contains(text(),'Thank you')]")


    def captcha_eval(self):
        captcha_text = self.captcha_to_eval.text
        result = eval(captcha_text)
        self.captcha.text = str(result)
        return self

    def set_rating(self, value):
        """Set the slider value reliably and verify it is applied."""
        slider = self.driver.find_element(By.XPATH, "//input[@matsliderthumb]")
        min_value = int(slider.get_attribute("min"))
        max_value = int(slider.get_attribute("max"))
        clamped_value = max(min_value, min(max_value, int(value)))

        # First try deterministic JS value set + events for Angular/Material listeners.
        self.driver.execute_script(
            """
            const slider = arguments[0];
            const target = String(arguments[1]);
            slider.focus();
            slider.value = target;
            slider.setAttribute('value', target);
            slider.dispatchEvent(new Event('input', { bubbles: true }));
            slider.dispatchEvent(new Event('change', { bubbles: true }));
            slider.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            slider,
            clamped_value,
        )

        if self._slider_value(slider) == clamped_value:
            return self

        # Fallback: drag/click interaction, then verify.
        width = slider.size["width"]
        offset = int((clamped_value - min_value) / (max_value - min_value) * width)
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(slider, 1, 1).click_and_hold().move_by_offset(offset, 0).release().perform()

        WebDriverWait(self.driver, 2).until(
            lambda _driver: self._slider_value(slider) == clamped_value
        )
        return self

    @staticmethod
    def _slider_value(slider):
        raw = slider.get_attribute("value") or slider.get_attribute("aria-valuenow")
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None

    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.comment.wait_until_visible()
        return self
