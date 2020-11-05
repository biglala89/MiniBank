## Mini Bank for Petty Cash

<b>Purpose of program</b>:

    This program simulates a mini bank that gives the users abilities to play as bank employee or customer.
    Employee can check customer's record and create accounts for customers.
    Customers are allowed to deposit, withdraw or check their own account balance.


<b>Mini Bank Entrance</b>:

    Personnel logins: employee or customer
 
For example:
```python
bs.employee_log_in(1, 'John', 'Dow')
bs.customer_log_in(100, 'Jane', 'Doe')
```


<b>Employee Methods</b>:

    Access employee basic information.
    Check customer in database: if no customer information, initialize a new record.
    Open account for customers and write new customer records to database.


<b>Customer Methods</b>:

    Check balance of their own accounts.    
    Deposit to withdraw from their accounts.    
    Transfer money between their own accounts.


<b>To Run in cmd</b>:

```python
from bank import Bank
bs = Bank()
```
