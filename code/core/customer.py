from database import CustomersDB
from validation import CustomerValidate
from employee import Employee


class Customer:
    """Create customer instances.
        Customers are given access to check their accounts' balances, make deposits, withdraws and fund-transfers as they wish.
        However customers should NOT be allowed writable-access to database.
        For simplicity, assume customer_id can be used by customer as an identifier when interacting with system.
    """
    __VALID_ACCOUTS = ['SAVINGS', 'CHECKINGS']

    def __init__(self, cust_id, first, last, db_name):
        self.__id = cust_id
        self.__first = first
        self.__last = last
        # need improvement to restrict customer access to database for malicious behaviors
        self.__database = CustomersDB(db_name)
        self.__database.establish_conn()
        self.__validator = CustomerValidate()

    def __repr__(self):
        return "Customer('{name}', customer_id: {cid})".format(name=self.fullname, cid=self.__id)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)

    def check_balance(self, acct_type):
        if self.__validator._is_active_customer(self.__id, self.__database) and self.__validator._is_valid_account(acct_type, self.__VALID_ACCOUTS):
            stmt = """SELECT C.CUSTOMER_ID, FIRST_NAME, LAST_NAME, ACCOUNT_TYPE, BALANCE 
                        FROM CUSTOMERS C 
                        INNER JOIN ACCOUNTS A 
                        ON C.CUSTOMER_ID = A.CUSTOMER_ID 
                        WHERE A.CUSTOMER_ID = {}
                        AND ACCOUNT_TYPE = '{}'
                    """.format(self.__id, acct_type.upper())
            return self.__database.query_records(stmt)

    def deposit(self, acct_type, amount):
        """Make deposit into customer's account
        """
        # check if a customer is active in the system and the deposit is a valid number
        cur_bal = self._get_balance(acct_type, amount)
        new_bal = cur_bal + amount
        print('Your new balance in {} is: ${}'.format(
            acct_type.upper(), new_bal))
        self.__update_balance(acct_type, new_bal)
        return new_bal

    def withdraw(self, acct_type, amount):
        """Withdraw from customer's account
        """
        cur_bal = self._get_balance(acct_type, amount)
        remaining_bal = cur_bal - amount
        try:
            self.__validator._is_valid_balance(remaining_bal)
            print('Remaining balance in {} is: ${}'.format(
                acct_type.upper(), remaining_bal))
            self.__update_balance(acct_type, remaining_bal)
            return (True, remaining_bal)
        except ValueError as e:
            print(e)
            print('Your {} balance remains the same: ${}'.format(
                acct_type.upper(), cur_bal))
            return (False, cur_bal)

    def transfer_funds(self, from_acct, to_acct, amount):
        if from_acct.upper() == to_acct.upper():
            raise KeyError(
                'Transfers between the same account are PROHIBITED!')
        withdraw_result, from_bal = self.withdraw(from_acct, amount)
        if withdraw_result:
            to_bal = self.deposit(to_acct, amount)
            print('\nNew balances: ({}: ${}), ({}: ${})'.format(
                from_acct.upper(), from_bal, to_acct.upper(), to_bal))
        else:
            to_bal = self._get_balance(to_acct, amount)
            print(to_bal)
            print('\nNew balances: ({}: ${}), ({}: ${})'.format(
                from_acct.upper(), from_bal, to_acct.upper(), to_bal))

    def _get_balance(self, acct_type, amount):
        if self.__validator.validate_inputs(self.__id, self.__database, acct_type, self.__VALID_ACCOUTS, amount):
            stmt = "SELECT BALANCE FROM ACCOUNTS WHERE CUSTOMER_ID = {} AND ACCOUNT_TYPE = '{}'".format(
                self.__id, acct_type.upper())
            return self.__database.query_records(stmt)[0][0]

    def __update_balance(self, acct_type, amount):
        stmt = """
                UPDATE ACCOUNTS
                SET BALANCE = {}
                WHERE CUSTOMER_ID = {}
                AND ACCOUNT_TYPE = '{}'
                """.format(amount, self.__id, acct_type.upper())
        try:
            self.__database.write_records(stmt)
        except ValueError as e:
            print(e)
            print('Transaction rolled back...')
