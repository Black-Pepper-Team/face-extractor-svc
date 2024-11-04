from .claim import Claim
from .participants import Participant
from .contest import Contest
from .db import db

def migrate_up() -> None:
    """
    The basic version of database migration
    """
    with db:
        db.create_tables([Claim, Participant, Contest])
        
def migrate_down() -> None:
    """
    Migrate down operation with dropping all tables
    """
    with db:
        db.drop_tables([Claim, Participant, Contest])
