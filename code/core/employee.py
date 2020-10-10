import logging
import os
import pandas as pd
from database import CustomersDB


class NamingError(ValueError):
    pass


class Employee:
    """Docstring
    """
    __valid_accounts = ['savings', 'checkings']

    def __init__(self, emp_id, first, last):
        self.__id = emp_id
        self.__first = first
        self.__last = last
        self.__database = CustomersDB('customers')

    def __repr__(self):
        return "Employee('{name}', employee_id: {eid})".format(name=self.fullname, eid=self.__id)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)

    # change name is not common, consider change address instead
    @fullname.setter
    def fullname(self, new_name):
        """Allows appropriate changes to this person's name if needed
        """
        if not isinstance(new_name, str):
            raise NamingError('Name can only be string')
        if len(new_name.split()) != 2:
            raise NamingError(
                'Please provide a full name separated with a space')
        self.__first, self.__last = new_name.split()
        return self.__first, self.__last

    def _retrive_records(self, stmt):
        self.__database.establish_conn()
        return self.__database.query_records(stmt)

    def check_customer(self, customer_id):
        """Looks up customer record
        """
        stmt = "select * from customers where customer_id = {}".format(
            customer_id)
        results = self._retrive_records(stmt)
        print(results)

        if len(results) == 0:
            return False
        return True

    def open_account(self, first_name, last_name, customer_id=None, acct_type=None, opening_deposit=0, valid_acct_types=__valid_accounts):
        """
        Opens account(s) for customer. Should not allow self-opened account(s)
        """
        # create a new method to validate all inputs
        if self._is_str_account(acct_type) or self._is_valid_account(acct_type) or self._is_valid_deposit(opening_deposit):
            print('entered block...')
            # a customer with an id should exist in our databse
            if customer_id:
                # retrive account type on file and figure out the other type to add
                stmt = "select account_type from accounts where customer_id = {}".format(
                    customer_id)
                existing_account = self._retrive_records(stmt)
                print(existing_account)
                if len(existing_account) == 0:
                    account_to_add = acct_type
                elif len(existing_account) == 2:
                    return 'No more accounts can be opened.'
                else:
                    account_to_add = valid_acct_types[existing_account not in valid_acct_types]
                print('Account to be added is: ', account_to_add)
                self._add_account(customer_id, acct_type, opening_deposit)
            elif customer_id is None:
                self._add_customer(customer_id, first_name, last_name)
                self._add_account(customer_id, acct_type, opening_deposit)

    def _add_customer(self, customer_id, first_name, last_name):
        stmt = "insert into customers values ({}, {}, {})".format(
            customer_id, first_name, last_name)
        self.__database.establish_conn()
        self.__database.write_records(stmt)

    def _add_account(self, customer_id, acct_type, opening_deposit):
        stmt = "insert into accounts values ({}, {}, {})".format(
            customer_id, acct_type, opening_deposit)
        self.__database.establish_conn()
        self.__database.write_records(stmt)

    def _is_str_account(self, acct_type):
        if not isinstance(acct_type, str):
            raise TypeError('Account type needs to be a string')
        return True

    def _is_valid_account(self, acct_type, valid_acct_types=__valid_accounts):
        if acct_type.lower() not in valid_acct_types:
            raise KeyError('Invalid account type!')
        return True

    def _is_valid_deposit(self, amount):
        if amount < 0:
            raise ValueError('Deposit can NOT be negative')
        return True
