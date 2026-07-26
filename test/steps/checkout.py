import time

from behave import step
from selenium.webdriver.support.ui import Select

from pageobjects.checkout import CheckoutPageObject


@step('I checkout products adding new address and card')
def step_impl(context):
    data = {row['param']: row['value'] for row in context.table}
    checkout = CheckoutPageObject()

    # Start checkout from the basket
    checkout.checkout_button.click()

    # Add a new delivery address
    checkout.add_address_panel.click()
    checkout.address_country.wait_until_visible()
    checkout.address_country.text = data['country']
    checkout.address_name.text = data['name']
    checkout.address_mobile_number.text = data['mobile']
    checkout.address_zip_code.text = data['zip']
    checkout.address_address.text = data['address']
    checkout.address_city.text = data['city']
    checkout.address_state.text = data['state']
    checkout.address_submit.wait_until_clickable()
    checkout.address_submit.click()

    # Select the newly added address and continue to delivery method
    checkout.select_address.click()
    checkout.proceed_button.click()
    

    # Choose a delivery speed and continue to payment
    checkout.delivery_speed.click()
    checkout.delivery_button.click()

    # Add a new payment card
    checkout.add_card_panel.click()
    checkout.card_name.wait_until_visible()
    checkout.card_name.text = data['name']
    checkout.card_number.text = data['card']
    month, year = data['expiry'].split('/')
    Select(checkout.card_expiry_month.find()).select_by_value(str(int(month.strip())))
    Select(checkout.card_expiry_year.find()).select_by_value('20' + year.strip())
    checkout.card_submit.click()

    # Select the newly added card and continue to review
    time.sleep(1)  # Wait for the card to be added and selectable
    checkout.payment_card.click()
    checkout.review_button.click()

    # Place the order
    checkout.checkout_button.click()
    time.sleep(2)
