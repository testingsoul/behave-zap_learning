@reuse_driver
Feature: CI Juice Shop Customer Feedback

  Background:  
    Given I open the Juice Shop

  @dast
  Scenario: Send Customer Feedback
    Given I go to customer feedback page
    When I send customer feedback form with comment "Great service!" and rating "5"
    Then I should see a success message

 
  Scenario: Customer Feedback button is disabled
    Given I go to customer feedback page
    When I fill customer feedback form without comment and rating "5"
    Then The submit button should be disabled