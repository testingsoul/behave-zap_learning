@reuse_driver
Feature: CI Juice Shop Login

  Background:  
    Given I open the Juice Shop
    
  Scenario: Login into Juice Shop with invalid user
    When I login into Juice Shop with user "fake_user" and password "Test@123"
    Then I should see an error message
    And I refresh the page

  Scenario: Login into Juice Shop without user
    When I login into Juice Shop without user and password "Test@123"
    Then the submit button is disabled
    And I refresh the page

  Scenario: Login into Juice Shop without password
    When I login into Juice Shop with user "test_user" and without password
    Then the submit button is disabled
    And I refresh the page

  @dast
  Scenario: Login into Juice Shop
    When I login into Juice Shop with default user
    Then the default user is logged in
    And I refresh the page