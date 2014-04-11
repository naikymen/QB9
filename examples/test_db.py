__author__ = 'naikymen'

from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase

#ERROR     "hstore type not found in the database. "
#peewee.ProgrammingError: hstore type not found in the database. please install it from your 'contrib/hstore.sql' file

DBNAME = 'test_db'

psql_db = PostgresqlExtDatabase(DBNAME, user='naikymen')
psql_db.get_conn().set_client_encoding('UTF8')


class CustomModel(Model):
    database = psql_db


class PtmID(CustomModel):
    ptmID = CharField()
    ptmAC = TextField()

PtmID.create_table()