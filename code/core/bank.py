from employee import Employee
from customer import Customer
from database import CustomersDB


class Bank:
    """Create a bank system that allows users to interact with.
    This is the main entrance to this bank system program.
    """

    def __init__(self):
        print('Welcome to ABC Bank! You must be logged in to proceed.')

    def employee_log_in(self, emp_id, first, last, db_name):
        """Authenticates employees
        """
        self.db = CustomersDB(db_name)
        self.db.establish_conn()
        self.db.construct_table()
        self.db.create_tables()
        # need to authenticate employee first and then returns instance
        # features needed here
        self.employee = Employee(emp_id, first, last, db_name)
        print('You are logged in as employee {}. Databse is ready.'.format(
            self.employee.__repr__()))
        return self.employee

    def customer_log_in(self, cust_id, first, last, db_name):
        """Allows customers to interact with the system"""
        self.db = CustomersDB(db_name)
        self.db.establish_conn()
        self.customer = Customer(cust_id, first, last, db_name)
        print('You are logged in as {}.'.format(self.customer.__repr__()))
        return self.customer
