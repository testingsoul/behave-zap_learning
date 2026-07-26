@reuse_driver
Feature: CI Juice Shop Create User

  Background: 
    Given I open the Juice Shop

  @dast
  Scenario: Create User Juice Shop
    Given I create user on Juice Shop
      | username | testuser@juice-sh.op |
      | password | Test@1234            |

