from database import CustomersDB
from validation import CustomerValidate
from employee import Employee


class Customer:
    """Customers should NOT be allowed writable-access to database, but basic query access is fine.
        For simplicity, assume customer_id can be used by customer as an identifier when interacting with system.
    """
    __VALID_ACCOUTS = ['SAVINGS', 'CHECKINGS']
    __TRANSFER_BETWEEN = {'CHECKINGS': (
        'SAVINGS', 'OTHER'), 'SAVINGS': ('CHECKINGS', 'OTHER')}
    __OUT_OF_NETWORK_TRANSFER_RATE = 0.001

    def __init__(self, cust_id, first, last, db_name):
        self.__id = cust_id
        self.__first = first
        self.__last = last
        # need improvement to restrict customer access to database for malicious behaviors
        self.__database = CustomersDB(db_name)
        self.__database.establish_conn()
        self.__CV = CustomerValidate()

    def __repr__(self):
        return "Customer('{name}', customer_id: {cid})".format(name=self.fullname, cid=self.__id)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)

    def check_balance(self, acct_type):
        if self.__CV._is_active_customer(self.__id, self.__database) and self.__CV._is_valid_account(acct_type, self.__VALID_ACCOUTS):
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
        cur_bal = self.__get_balance(acct_type, amount)
        new_bal = cur_bal + amount
        return 'Your new balance is: ${}'.format(new_bal)
        # update_record()

    def withdraw(self, acct_type, amount):
        """Withdraw from customer's account
        """
        cur_bal = self.__get_balance(acct_type, amount)
        remaining_bal = cur_bal - amount
        try:
            self.__CV._is_valid_balance(remaining_bal)
            print('Remaining balance in {} is: ${}'.format(
                acct_type, remaining_bal))
        except ValueError as e:
            print(e)
            return 'Your balance remains the same: ${}'.format(cur_bal)
        # update_record()

    def transfer_funds(self, from_, to_, amount):
        pass

    def __get_balance(self, acct_type, amount):
        if self.__CV.validate_inputs(self.__id, self.__database, acct_type, self.__VALID_ACCOUTS, amount):
            stmt = "SELECT BALANCE FROM ACCOUNTS WHERE CUSTOMER_ID = {} AND ACCOUNT_TYPE = '{}'".format(
                self.__id, acct_type.upper())
            return self.__database.query_records(stmt)[0][0]
