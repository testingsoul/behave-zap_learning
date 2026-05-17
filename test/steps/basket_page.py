import time

from behave import step

from pageobjects.basket_page import BasketPageObject


@step('I delete item from basket')
def step_impl(context):
    BasketPageObject().delete_item.click()
    time.sleep(2)

    

@step('I sum an item in the basket')
def step_impl(context):
    BasketPageObject().sum_item.click()
    time.sleep(2)