class Customers:

    def __repr__(self):
        return "Customer('{name}', email: {email}, current address: {address})".format(name=self.fullname, email=self.__email, address=self.__address)

    @property
    def fullname(self):
        """Returns full name of the person
        """
        return '{} {}'.format(self.__first, self.__last)
