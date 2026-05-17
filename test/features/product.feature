@reuse_driver
Feature: CI Juice Shop Product Management

  Background: 
    Given I open the Juice Shop
    And I login into Juice Shop with default user

  @dast
  Scenario: Search and add product
    Given I search for "Apple Juice"
    Given I add item to cart

  @dast
  Scenario: Increase product
    Given I open basket page
    Given I sum an item in the basket

  @dast
  Scenario: Delete product
    Given I open basket page
    Given I delete item from basket




