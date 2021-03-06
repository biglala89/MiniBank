import logging
from database import CustomersDB
from validation import Validate


class Employee:
    """Create employee instances.
        Employees are given access to look up customer's account information, open accounts for customers to update customer database.
    """

    __VALID_ACCOUNTS = ['SAVINGS', 'CHECKINGS']

    def __init__(self, emp_id, first, last, db_name):
        self.__id = emp_id
        self.__first = first
        self.__last = last
        self.__database = CustomersDB(db_name)
        self.__database.establish_conn()
        self.__validator = Validate()

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

        # make sure all the inputs are valid
        if self.__validator.validate_inputs(first_name, last_name, acct_type, self.__VALID_ACCOUNTS, opening_deposit):

            # a customer with an id should exist in our databse
            if customer_id:

                # retrive account type on file and determine the right account to add
                stmt = "SELECT ACCOUNT_TYPE FROM ACCOUNTS WHERE CUSTOMER_ID = {}".format(
                    customer_id)
                existing_account = self._retrive_records(stmt)
                print('Records show customer has {} in the system'.format(
                    existing_account))

                # even if customer_id is provided, if account shows zero record, customer needs to be initialized in the system first
                if len(existing_account) == 0:
                    account_to_add = acct_type
                    self._add_customer(customer_id, first_name, last_name)
                elif len(existing_account) == len(self.__VALID_ACCOUNTS):
                    return 'No more accounts can be opened at this time.'
                else:
                    print(
                        'This account has already been opened, we will open another account for you')

                    available_accts = set(self.__VALID_ACCOUNTS) - \
                        set(existing_account[0])
                    account_to_add = available_accts.pop()

                print('Account to be added is: ', account_to_add)
                self._add_account(customer_id, account_to_add, opening_deposit)

            # for new customer with no customer_id create customer record and open an account
            elif customer_id is None:
                self._add_customer(customer_id, first_name, last_name)
                self._add_account(customer_id, acct_type, opening_deposit)

    def _add_customer(self, customer_id, first_name, last_name):
        stmt = "INSERT INTO CUSTOMERS VALUES ('{}', '{}', '{}')".format(
            customer_id, first_name.upper(), last_name.upper())
        self.__database.write_records(stmt)

    def _add_account(self, customer_id, acct_type, opening_deposit):
        stmt = "INSERT INTO ACCOUNTS VALUES ('{}', '{}', '{}')".format(
            customer_id, acct_type.upper(), opening_deposit)
        self.__database.write_records(stmt)
