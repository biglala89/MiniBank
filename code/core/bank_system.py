from employee import Employee
from database import CustomersDB


class Bank:
    def __init__(self):
        # self.db = CustomersDB('customers')
        # self.db.establish_conn()
        # self.db.construct_table()
        # self.db.create_tables()
        print('Welcome to ABC Bank! Database is ready to use. You must be logged in to proceed.')

    def employee_log_in(self, emp_id, first, last):
        """Authenticates employees"""
        # need to authenticate employee first and then returns instance
        # features needed here
        self.employee = Employee(emp_id, first, last)
        return self.employee

    def customer_log_in(self):
        """Allows customers to interact with the system"""
        pass
