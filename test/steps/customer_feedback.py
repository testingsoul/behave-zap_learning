import time

from behave import step

from pageobjects.customer_feedback import CustomerFeedbackPageObject
from selenium.common.exceptions import TimeoutException


@step('I send customer feedback form with comment "{comment}" and rating "{rating}"')
def step_impl(context, comment="Test comment", rating=5):
    CustomerFeedbackPageObject().comment.text = comment
    CustomerFeedbackPageObject().set_rating(int(rating))
    CustomerFeedbackPageObject().captcha_eval()
    CustomerFeedbackPageObject().submit.click()
    time.sleep(1)  # Wait for the form submission to complete

@step('I fill customer feedback form without comment and rating "{rating}"')
def step_impl(context, rating=5):
    CustomerFeedbackPageObject().set_rating(int(rating))
    CustomerFeedbackPageObject().captcha_eval()

@step('I should see a success message')
def step_impl(context):
    try:
        CustomerFeedbackPageObject().success_message.wait_until_visible(timeout=2)
    except TimeoutException:
        assert False, "Success message not displayed"

@step('The submit button should be disabled')
def step_impl(context):
    try:
        CustomerFeedbackPageObject().submit.wait_until_clickable(timeout=0.1)
        assert False, "Submit button is not disabled"
    except TimeoutException:
        pass  # Button is disabled as expected
