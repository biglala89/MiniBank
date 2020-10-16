from employee import Employee
from customer import Customer
from database import CustomersDB


class Bank:
    """Create a bank system that allows users to interact with.
    This is the main entrance to this bank system program.
    """
    __DEFAULT_DB = 'ABC_Bank_Customers'

    def __init__(self):
        self.db = CustomersDB(self.__DEFAULT_DB)
        self.db.establish_conn()
        self.db.construct_table()
        self.db.create_tables()
        print('Welcome to ABC Bank! You must be logged in to proceed.')

    def employee_log_in(self, emp_id, first, last, db_name=__DEFAULT_DB):
        """Authenticates employees
        """
        self.employee = Employee(emp_id, first, last, db_name)
        print('You are logged in as employee {}. Databse is ready.'.format(
            self.employee.__repr__()))
        return self.employee

    def customer_log_in(self, cust_id, first, last, db_name=__DEFAULT_DB):
        """Allows customers to interact with the system
        """
        self.customer = Customer(cust_id, first, last, db_name)
        print('You are logged in as {}.'.format(self.customer.__repr__()))
        return self.customer
