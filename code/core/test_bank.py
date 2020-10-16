import bank
import pytest
from validation import IndentityError

bank = bank.Bank()
emp = bank.employee_log_in(1, 'Barack', 'Obama')


def test_employee_log_in():
    assert emp.fullname == 'Barack Obama'


def test_employee_check_customer():
    # customer with id = 1 is in the database
    assert emp.check_customer(1) == False

    # customer with id = 100 is not in the database
    assert emp.check_customer(100) == False


def test_employee_open_account():
    # non-string name should raise TypeError exception
    with pytest.raises(TypeError):
        emp.open_account(123, 'Obama', 2, 'savings', 100)

    # invalid account type should raise KeyError exception
    with pytest.raises(KeyError):
        emp.open_account('Michelle', 'Obama', 2, 'savvvvings', 100)

    # negative deposit should raise ValueError exception
    with pytest.raises(ValueError):
        emp.open_account('Michelle', 'Obama', 2, 'savings', -100)


def test_employee_open_invalid_account():
    # open an savings account for a new customer
    emp.open_account('John', 'Doe', 10, 'savings', 9000)

    # open another checkings account for the same customer
    emp.open_account('John', 'Doe', 10, 'checkings', 5000)

    # no more available accounts can be opened for this
    # customer after both allowed accounts have been created
    assert emp.open_account('John', 'Doe', 10, 'savings',
                            7000) == 'No more accounts can be opened at this time.'


def test_customer_log_in():
    cus = bank.customer_log_in(2, 'John', 'Doe')
    assert cus.fullname == 'John Doe'


def test_wrong_customer_check_balance():
    cus = bank.customer_log_in(20, 'John', 'Doe')

    # customer with wrong customer_id and name combination
    # should raise IndentityError exception
    with pytest.raises(IndentityError):
        cus.check_balance('savings')


def test_customer_check_wrong_balance():
    cus = bank.customer_log_in(10, 'john', 'doe')

    # invalid account type should raise exception
    with pytest.raises(KeyError):
        cus.check_balance('other')

    with pytest.raises(TypeError):
        cus.check_balance(4321)


def test_customer_transfer_invalid_funds():
    cus = bank.customer_log_in(10, 'John', 'Doe')

    # transfer between the same account should raise KeyError exception
    with pytest.raises(KeyError):
        cus.transfer_funds('savings', 'savings', 1000)

    # transfer with invalid amount should raise ValueError exception
    with pytest.raises(ValueError):
        cus.transfer_funds('savings', 'checkings', -1000)

    # transfer with invalid account type should raise KeyError exception
    with pytest.raises(KeyError):
        cus.transfer_funds('savings', 'invalid_account', 1000)


def test_customer_transfer_funds():
    """This test function should also validate both deposit 
        and withdraw methods as both methods are called 
        within transfer_funds function.
    """
    cus = bank.customer_log_in(10, 'John', 'Doe')
    from_account = 'savings'
    to_account = 'checkings'
    tran_amt = 1000
    # get new balance result by calling transfer function
    new_balances = cus.transfer_funds(from_account, to_account, tran_amt)

    # work out each account's current balance
    cur_from_bal = cus._get_balance(from_account, tran_amt)
    cur_to_bal = cus._get_balance(to_account, tran_amt)

    # put balances in right form for assertion
    cur_balances = (cur_from_bal, cur_to_bal)

    assert cur_balances == new_balances
