from employee import Employee


class Bank:
    def __init__(self):
        print('Welcome to ABC Bank. You must be logged in to proceed.')

    def employee_log_in(self, emp_id, first, last):
        """Authenticates employees"""
        # need to authenticate employee first and then returns instance
        # features needed here
        self.employee = Employee(emp_id, first, last)
        return self.employee

    def customer_log_in(self):
        """Allows customers to interact with the system"""
        pass
