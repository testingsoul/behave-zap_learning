import time

from behave import step

from pageobjects.complaint import ComplaintPageObject
from selenium.common.exceptions import TimeoutException


@step('I send complaint with message "{message}" and invoice')
def step_impl(context, message="Test complaint"):
    ComplaintPageObject().message.text = message
    ComplaintPageObject().upload_invoice()
    ComplaintPageObject().submit.click()
    time.sleep(1)  # Wait for the form submission to complete

@step('I should see a complaint success message')
def step_impl(context):
    try:
        ComplaintPageObject().success_message.wait_until_visible(timeout=2)
    except TimeoutException:
        assert False, "Success message not displayed"

@step('the complaint submit button should be disabled')
def step_impl(context):
    try:
        ComplaintPageObject().submit.wait_until_clickable(timeout=0.1)
        assert False, "Submit button is not disabled"
    except TimeoutException:
        pass  # Button is disabled as expected
