class Validate:
    """Make sure inputs are valid
    """

    def validate_inputs(self, first_name, last_name, acct_type, valid_acct, opening_deposit):
        return self._is_valid_name(first_name, last_name) and self._is_valid_account(acct_type, valid_acct) and self._is_valid_deposit(opening_deposit)

    def _is_valid_name(self, first_name, last_name):
        if not isinstance(first_name, str) or not isinstance(last_name, str):
            raise TypeError(
                'Please enter a valid name! Names must be strings.')
        return True

    def _is_valid_account(self, acct_type, valid_acct):
        if not isinstance(acct_type, str):
            raise TypeError('Account type needs to be a string!')
        if acct_type.lower() not in valid_acct:
            raise KeyError('Invalid account type!')
        return True

    def _is_valid_deposit(self, amount):
        if amount < 0:
            raise ValueError('Deposit can NOT be negative!')
        return True
