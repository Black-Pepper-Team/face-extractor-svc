import peewee
from playhouse.postgres_ext import *

from .db import BaseModel

class Contest(BaseModel):
    id = peewee.BigAutoField(primary_key=True)
