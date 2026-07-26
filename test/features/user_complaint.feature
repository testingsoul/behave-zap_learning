@reuse_driver
Feature: CI Juice Shop Complaint

  Background:
    Given I open the Juice Shop
    And I login into Juice Shop with default user

  @dast
  Scenario: Send a complaint with message and invoice
    Given I go to complaint page
    When I send complaint with message "The apple juice bottle arrived leaking" and invoice
    Then I should see a complaint success message

  Scenario: Complaint submit button is disabled without message
    Given I go to complaint page
    Then the complaint submit button should be disabled
