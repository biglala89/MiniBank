from employee import Employee


# class Customers(People, Accounts, Services): pass


class NamingError(ValueError):
    pass


class Customers(Employee):

    def __repr__(self):
        return "Customer('{name}', email: {email}, current address: {address})".format(name=self.fullname, email=self.__email, address=self.__address)

    @property
    def identity(self):
        return 'I am a customer. My name is {}'.format(self.fullname)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)

    # change name is not common, consider change address instead
    @fullname.setter
    def fullname(self, new_name):
        """Allows appropriate changes to this person's name if needed
        """
        if not isinstance(new_name, str):
            raise NamingError('Name can only be string')
        if len(new_name.split()) != 2:
            raise NamingError(
                'Please provide a full name separated with a space')
        self.__first, self.__last = new_name.split()
        return self.__first, self.__last

        # @property
        # def address(self):
        #     return self.__address

        # @address.setter
        # def address(self, new_address):
        #     self._update_address(new_address)

        # def _update_address(self, new_address):
        #     self.__address = new_address
        #     print('Address has been updated to: {}'.format(self.__address))
        #     return self.__address

        # @property
        # def email(self):
        #     return self.__email

        # @email.setter
        # def email(self, new_email):
        #     self.__email = new_email

        # @classmethod
        # def from_file(cls, file):
        #     """
        #     Creates person entity from file
        #     """
        #     with open(file, 'r') as f:
        #         content = f.read()
        #         emp_id, first, last = map(
        #             lambda x: x.strip(), content.split('|'))
        #     return cls(emp_id, first, last)
