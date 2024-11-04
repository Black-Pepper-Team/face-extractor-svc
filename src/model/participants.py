import peewee
from playhouse.postgres_ext import *

from .db import BaseModel

from .contest import Contest

class Participant(BaseModel):
    image_hash = peewee.FixedCharField(max_length=66)
    image_content = peewee.BlobField()
    name = peewee.CharField()
    reward_address = peewee.CharField()
    proof = JSONField()
    feature_vector = ArrayField(peewee.IntegerField)
    contest = peewee.ForeignKeyField(Contest)

    class Meta:
        primary_key = CompositeKey('contest', 'image_hash')
