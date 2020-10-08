import logging
import os
import pandas as pd


class NamingError(ValueError):
    pass


class Employee:
    """Docstring
    """
    # __current_path = os.getcwd()
    __customer_records = '../data/customer_data.csv'
    __customer_acct = '../data/customer_acct.csv'
    __valid_accounts = ['savings', 'checkings']

    def __init__(self, emp_id, first, last):
        self.__id = emp_id
        self.__first = first
        self.__last = last

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

    def _read_file(self, file):
        return pd.read_csv(file)

    def check_customer(self, customer_id, customer_file=__customer_records):
        """Looks up customer record
        """
        customer_table = self._read_file(customer_file)
        # customer_table = pd.read_csv(customer_file)
        customer_table.set_index('customer_id')
        if customer_id <= customer_table['customer_id'].max():
            print(customer_table[customer_table['customer_id'] == customer_id])
            return True
        else:
            print('Customer not found')
            return False

    def open_account(self, customer_id, first_name, last_name, acct_type=None, opening_deposit=0,
                     cust_acct=__customer_acct, cust_data=__customer_records, valid_acct_types=__valid_accounts):
        """
        Opens account(s) for customer. Should not allow self-opened account(s)
        """
        # create a new method to validate all inputs
        if self._is_str_account(acct_type) and self._is_valid_account(acct_type) and self._is_valid_deposit(opening_deposit):
            print('entered block...')
            customer_table = self._read_file(cust_acct)
            if len(customer_table) == 0:
                customer_id = 1
                self.__add_customer_record(customer_id, first_name, last_name)
                self.__add_account_info(
                    customer_id, acct_type, opening_deposit)
            else:
                account_records = customer_table[customer_table['customer_id']
                                                 == customer_id]
                if len(account_records) == 0:
                    customer_id = account_records['customer_id'].max() + 1
                    self.__add_customer_record(
                        customer_id, first_name, last_name)
                    self.__add_account_info(
                        customer_id, acct_type, opening_deposit)
                # what if allowed types are more than two? consider how to cope with it
                elif len(account_records) == 1:
                    new_acct_type = valid_acct_types - \
                        set(account_records['account_type'].unique())
                    self.__add_account_info(
                        customer_id, new_acct_type, opening_deposit)
                else:
                    print('All available accounts have been set up.')

    def __add_customer_record(self, new_cust_id, new_first, new_last, dstn_file=__customer_records):
        new_rows = pd.DataFrame(
            [{new_cust_id, new_first, new_last}], columns=['customer_id', 'first_name', 'last_name'])
        new_rows.to_csv(dstn_file, index=False, header=False, mode='a')

    def __add_account_info(self, new_cust_id, acct_type, opening_deposit, dstn_file=__customer_acct):
        new_rows = pd.DataFrame(
            [{new_cust_id, acct_type, opening_deposit}], columns=['customer_id', 'account_type', 'balance'])
        new_rows.to_csv(dstn_file, index=False, header=False, mode='a')

    def _is_str_account(self, acct_type):
        if not isinstance(acct_type, str):
            raise ValueError('Account type needs to be a string')
        return True

    def _is_valid_account(self, acct_type, valid_acct_types=__valid_accounts):
        if acct_type.lower() not in valid_acct_types:
            raise ValueError('Invalid account type!')
        return True

    def _is_valid_deposit(self, amount):
        if amount < 0:
            raise ValueError('Deposit can not be negative')
        return True
