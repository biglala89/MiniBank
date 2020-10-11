import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey, Index
from sqlalchemy.schema import UniqueConstraint


class Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.dstn = '../../data_src'
        self.engine = create_engine(
            'sqlite:///{}/{}.db'.format(self.dstn, self.db_name))
        self.connection = None
        self.metadata = MetaData()

    def establish_conn(self):
        self.connection = self.engine.connect()
        return self.connection

    def construct_table(self):
        self.tables = []
        return self.tables

    def create_tables(self):
        if not self.tables:
            return
        for table in self.tables:
            table.create(self.engine, checkfirst=True)

    def query_records(self, stmt):
        results = self.connection.execute(stmt).fetchall()
        return results

    def write_records(self, stmt):
        result_proxy = self.connection.execute(stmt)
        return result_proxy.rowcount

    def print_tablenames(self):
        return self.engine.table_names()


class CustomersDB(Database):

    def __init__(self, db_name):
        super().__init__(db_name)

    def construct_table(self):
        customer_accounts = Table('customers', self.metadata,
                                  Column('customer_id', Integer(),
                                         primary_key=True, unique=True),
                                  Column('first_name', String(30)),
                                  Column('last_name', String(30)),
                                  keep_existing=True
                                  )

        customer_records = Table('accounts', self.metadata,
                                 Column('customer_id', Integer(), ForeignKey(
                                     'customers.customer_id')),
                                 Column('account_type', String(20)),
                                 Column('balance', Float(), nullable=True),
                                 #  UniqueConstraint(
                                 #      ('customer_id', 'account_type'), name='cust_acct'),
                                 keep_existing=True
                                 )

        # CREATE COMPOSITE KEY FIRST!!!
        # Index('myindex', self.db_name.customer_records.customer_id,
        #       self.db_name.customer_records.account_type, unique=True)

        self.tables = [customer_accounts, customer_records]
        return self.tables
