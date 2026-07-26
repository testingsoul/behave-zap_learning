import time

from behave import step

from pageobjects.login import LoginPageObject
from selenium.common.exceptions import TimeoutException

@step('I open the Juice Shop')
def step_impl(context):
    
    LoginPageObject().open()
    time.sleep(1)  # Wait for the login to complete

@step('I login into Juice Shop with default user')
def step_impl(context):
    
    LoginPageObject().login()
    time.sleep(1)  # Wait for the login to complete

@step('I login into Juice Shop with user "{username}" and password "{password}"')
@step('I login into Juice Shop without user and password "{password}"')
@step('I login into Juice Shop with user "{username}" and without password')
def step_impl(context, username="", password=""):
    LoginPageObject().login(username, password)
    time.sleep(2)  # Wait for the login to complete

@step('the submit button is disabled')
def step_impl(context):
    try:
        LoginPageObject().submit.wait_until_clickable(timeout=0.1)
        assert False, "Submit button is not disabled"
    except TimeoutException:
        pass  # Button is disabled as expected

@step('I should see an error message')
def step_impl(context):
    assert LoginPageObject().error_message.wait_until_visible(timeout=2), "Error message not displayed"


@step('the default user is logged in')
def step_impl(context):
    # Implement the step to verify the default user is logged in
    pass

@step('I create user on Juice Shop')
def step_impl(context):
    if context.table:
        user = dict([context.table.headings] + [row.cells for row in context.table.rows])
        LoginPageObject().create_user(user.get('username'), user.get('password'))
    else:
        LoginPageObject().create_user()
    time.sleep(2)  # Wait for the login to complete


