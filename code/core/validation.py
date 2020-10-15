class IndentityError(ValueError):
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
            raise ValueError(
                'Insuffient fund available for this transaction. Transaction cancelled.')
        return True


class CustomerValidate(Validate):
    """Extend validations for customer instances.
    """

    def validate_inputs(self, customer_id, db, acct_type, valid_acct, opening_deposit):
        return self._is_active_customer(customer_id, db) and \
            self._is_valid_account(acct_type, valid_acct) and \
            self._is_valid_deposit(opening_deposit)

    def _is_active_customer(self, customer_id, db):
        stmt = "SELECT CUSTOMER_ID FROM CUSTOMERS"
        active_ids = db.query_records(stmt)
        if customer_id not in set(map(lambda x: x[0], active_ids)):
            raise IndentityError(
                "Our system shows no record for this customer")
        return True
