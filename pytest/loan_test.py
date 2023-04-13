# test_app.py

# assert expression
## if true nothing happens
## if false raises AssertionError

# create virtual environment and activate
# pip install pytest
# pip install pytest-cov

# run tests with python -m pytest -s
# compare -s and -v when running the tests
# run coverage tests with python -m pytest --cov

import pytest
from oop_loan_pmt import *


@pytest.fixture
def client():
    with Loan.test_client() as client:
        yield client

# # Unit Tests
def test_loan_discount_factor():
    """
    GIVEN a user enters their loan details
    WHEN the loan object's calculateDiscountFactor method is called
    THEN the discount factor is accurately calculated
    """
    loan = Loan(loanAmount=100000, numberYears=30, annualRate=0.06)
    loan.calculateDiscountFactor()
    print("\r")
    print(" -- calculateDiscountFactor method unit test")
    assert loan.getDiscountFactor() == pytest.approx(
        166.79, rel=1e-3
    )  # approx two decimal places


def test_loan_payment():
    """
    GIVEN a user enters their loan details
    WHEN the loan object's calculateLoanPmt method is called
    THEN the loan payment is accurately calculated
    """
    loan = Loan(loanAmount=100000, numberYears=30, annualRate=0.06)
    loan.calculateLoanPmt()
    print("\r")
    print(" -- calculateLoanPmt method unit test")
    assert loan.getLoanPmt() == pytest.approx(
        599.55, rel=1e-3
    )  # approx two decimal places

# Functional Tests
def test_collectLoanDetails(monkeypatch):
    """
    GIVEN a user inputs their loan details
    WHEN the collectLoanDetails function is called
    THEN the input it collected and put into the other functions
    """
    input_values = ["100000", "30", "0.06"]
    def mock_input(s):  # using mock_input and monkeypatch to simulate user input using my input values above to test the function
        return input_values.pop(0)
    monkeypatch.setattr('builtins.input', mock_input)
    print("\r")
    print(" -- collectLoanDetails functional test")
    loan = collectLoanDetails()
    expected_values = (100000, 30, 0.06)
    actual_values = (loan.loanAmount, loan.numberOfPmts / 12, loan.annualRate)
    assert expected_values==actual_values



def test_main(monkeypatch, capsys):
    """
    GIVEN the user has inputted their loan details
    WHEN the main function is called
    THEN the loan details are ran through all functions and are printed in the statement below
    """
    input_values = ['100000', '30', '0.06\n'] # set the input values
    def mock_input(s):
        return input_values.pop(0)
    monkeypatch.setattr('builtins.input', mock_input) # replace input() with mock function
    
    main() # call the main function

    captured = capsys.readouterr() # capture the output
    assert captured.out == 'Your monthly payment is: $599.55\n'

    