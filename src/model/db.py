import peewee
from playhouse.postgres_ext import *

db = peewee.PostgresqlDatabase('face', user='face', password='face', host='127.0.0.1', port=15432)

class BaseModel(peewee.Model):
    class Meta:
        database = db
