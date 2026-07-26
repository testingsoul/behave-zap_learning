@reuse_driver
Feature: CI Juice Shop Product Checkout

  Background: 
    Given I open the Juice Shop
    And I login into Juice Shop with default user
    And I search for "Apple Juice"
    And I add item to cart

  @dast
  Scenario: Checkout products adding new address and card
    Given I open basket page
    Given I checkout products adding new address and card
      | param   | value            |
      | country | United States    |
      | name    | John Doe2        |
      | mobile  | 1234567890       |
      | zip     | 12345            |
      | address | 123 Main St      |
      | city    | Anytown2         |
      | state   | California       |
      | card    | 4111111111111113 |
      | expiry  | 12/85            |
