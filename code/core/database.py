import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey

# os.chdir('/Users/chowli/Documents/Springboard_DE/Projects/mini-projects/Banking_System/data_src')
# engine = create_engine('sqlite:///customers.db')
# metadata = MetaData()
# metadata.create_all(engine)
# print(engine.table_names())


class database:

    def __init__(self, db_name):
        self.db_name = db_name
        # self.src = '/Users/chowli/Documents/Springboard_DE/Projects/mini-projects/Banking_System/data_src'
        self.engine = create_engine('sqlite:///{}.db'.format(self.db_name))
        self.metadata = MetaData()
        self.tables = None

    def construct_table(self, table_name):
        # define a table constructor method instead
        if not self.tables:
            self.tables = []

        customer_accounts = Table('customer_accounts', self.metadata,
                                  Column('customer_id', Integer(),
                                         primary_key=True),
                                  Column('first_name', String(30)),
                                  Column('last_name', String(30)),
                                  keep_existing=True
                                  )

        customer_records = Table('customer_records', self.metadata,
                                 Column('customer_id', Integer(), ForeignKey(
                                     'customer_accounts.customer_id')),
                                 Column('account_type', String(20)),
                                 Column('balance', Float()),
                                 keep_existing=True
                                 )

        self.tables = [customer_accounts, customer_records]
        return self.tables

    def create_tables(self):
        if not self.tables:
            return
        for table in self.tables:
            table.create(self.engine, checkfirst=True)

    def query_records(self, table_name):
        connection = self.engine.connect()
        stmt = 'select * from {}'.format(str(table_name))
        results = connection.execute(stmt).fetchall()
        return results

    def write_records(self):
        pass

    def print_tablenames(self):
        print(self.engine.table_names())
