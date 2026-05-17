import time

from behave import step

from pageobjects.login import LoginPageObject
from pageobjects.main_page import MainPagePageObject


@step('I go to customer feedback page')
def step_impl(context):
    MainPagePageObject().side_menu.click()
    MainPagePageObject().customer_feedback.click()
    

@step('I search for "{search_term}"')
def step_impl(context, search_term):
    MainPagePageObject().home.click()
    MainPagePageObject().search_button.click()
    MainPagePageObject().search.text = search_term
    time.sleep(1)  # Wait for the search results to load

@step('I add item to cart')
def step_impl(context):
    MainPagePageObject().add_first_visible_product_to_cart()
    time.sleep(2)

@step('I open basket page')
def step_impl(context):
    MainPagePageObject().basket.click()

@step('I refresh the page')
def step_impl(context):
    context.driver.refresh()
