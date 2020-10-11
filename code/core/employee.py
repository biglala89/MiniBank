import logging
import os
import pandas as pd
from database import CustomersDB


class NamingError(ValueError):
    pass


class Employee:
    """Docstring
    """
    __VALID_ACCOUNTS = ['savings', 'checkings']

    def __init__(self, emp_id, first, last):
        self.__id = emp_id
        self.__first = first
        self.__last = last
        self.__database = CustomersDB('customers')
        self.__database.establish_conn()

    def __repr__(self):
        return "Employee('{name}', employee_id: {eid})".format(name=self.fullname, eid=self.__id)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)

    def _retrive_records(self, stmt):
        return self.__database.query_records(stmt)

    def check_customer(self, customer_id):
        """Looks up customer record
        """
        stmt = "SELECT * FROM CUSTOMERS WHERE CUSTOMER_ID = {}".format(
            customer_id)
        results = self._retrive_records(stmt)
        print(results)

        if len(results) == 0:
            return False
        return True

    def open_account(self, first_name, last_name, customer_id=None, acct_type=None, opening_deposit=0):
        """
        Opens account(s) for customer. Should not allow self-opened account(s)
        """
        # validate all inputs
        if self._is_str_account(acct_type) and self._is_valid_account(acct_type) and self._is_valid_deposit(opening_deposit):

            # a customer with an id should exist in our databse
            if customer_id:
                # retrive account type on file and figure out the right account to add
                stmt = "SELECT ACCOUNT_TYPE, BALANCE FROM ACCOUNTS WHERE CUSTOMER_ID = {}".format(
                    customer_id)
                existing_account = self._retrive_records(stmt)
                print('Records show customer has {} in the system'.format(
                    existing_account))

                # even if customer_id is provided, if record shows zero account, customer needs to be initialized in the system first
                if len(existing_account) == 0:
                    account_to_add = acct_type
                    self._add_customer(customer_id, first_name, last_name)

                elif len(existing_account) == len(self.__VALID_ACCOUNTS):
                    return 'No more accounts can be opened.'

                else:
                    account_to_add = self.__VALID_ACCOUNTS[existing_account not in self.__VALID_ACCOUNTS]
                print('Account to be added is: ', account_to_add)
                self._add_account(customer_id, acct_type, opening_deposit)

            elif customer_id is None:
                self._add_customer(customer_id, first_name, last_name)
                self._add_account(customer_id, acct_type, opening_deposit)

    def _add_customer(self, customer_id, first_name, last_name):
        stmt = "INSERT INTO CUSTOMERS VALUES ('{}', '{}', '{}')".format(
            customer_id, first_name, last_name)
        self.__database.write_records(stmt)

    def _add_account(self, customer_id, acct_type, opening_deposit):
        stmt = "INSERT INTO ACCOUNTS VALUES ('{}', '{}', '{}')".format(
            customer_id, acct_type, opening_deposit)
        self.__database.write_records(stmt)

    def _is_str_account(self, acct_type):
        if not isinstance(acct_type, str):
            raise TypeError('Account type needs to be a string')
        return True

    def _is_valid_account(self, acct_type):
        if acct_type.lower() not in self.__VALID_ACCOUNTS:
            raise KeyError('Invalid account type!')
        return True

    def _is_valid_deposit(self, amount):
        if amount < 0:
            raise ValueError('Deposit can NOT be negative')
        return True
