import peewee
from typing import List

from .db import BaseModel

class Claim(BaseModel):
    id = peewee.PrimaryKeyField()
    metadata = peewee.TextField()
    vector = peewee.TextField()
    pk = peewee.TextField()
    user_id = peewee.TextField(unique=True)
    claim_id = peewee.TextField()
    is_submitted = peewee.BooleanField()
        
def select_all_claims() -> List[Claim]:
    """
    Selects all claims from the database
    """
    
    return [claim for claim in Claim.select().dicts()]
