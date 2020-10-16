class IndentityError(ValueError):
    pass


class BalanceError(ValueError):
    pass


class Validate:
    """Make sure inputs are valid
    """

    def validate_inputs(self, first_name, last_name, acct_type, valid_acct, opening_deposit):
        return self._is_valid_name(first_name, last_name) and \
            self._is_valid_account(acct_type, valid_acct) and \
            self._is_valid_deposit(opening_deposit)

    def _is_valid_name(self, first_name, last_name):
        if not isinstance(first_name, str) or not isinstance(last_name, str):
            raise TypeError(
                'Please enter a valid name! Names must be strings.')
        return True

    def _is_valid_account(self, acct_type, valid_acct):
        if not isinstance(acct_type, str):
            raise TypeError('Account type needs to be a string!')
        if acct_type.upper() not in valid_acct:
            raise KeyError('Invalid account type!')
        return True

    def _is_valid_deposit(self, amount):
        if amount <= 0:
            raise ValueError('Deposit must be positive!')
        return True

    def _is_valid_balance(self, balance):
        if balance < 0:
            raise BalanceError(
                'Insuffient fund available for this transaction. Transaction cancelled.')
        return True


class CustomerValidate(Validate):
    """Extend validations for customer instances.
    """

    def validate_inputs(self, customer_id, first_name, last_name, db, acct_type, valid_acct, opening_deposit):
        return self._is_valid_customer(customer_id, first_name, last_name, db) and \
            self._is_valid_account(acct_type, valid_acct) and \
            self._is_valid_deposit(opening_deposit)

    def _is_valid_customer(self, customer_id, first_name, last_name, db):
        stmt = "SELECT FIRST_NAME, LAST_NAME FROM CUSTOMERS WHERE CUSTOMER_ID = {}".format(
            customer_id)
        res = db.query_records(stmt)
        if not res:
            raise IndentityError(
                "Our system shows no record for this customer_id!")
        res_first_name, res_last_name = res[0]
        if res_first_name != first_name.upper() or res_last_name != last_name.upper():
            raise IndentityError(
                "Customer name does not match records on file!")
        return True
