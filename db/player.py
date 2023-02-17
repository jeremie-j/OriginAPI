import sqlalchemy as sa
from db.engine import engine
from models.player import pla


def get_by_id(account_id: int):
    with engine.begin() as conn:
        stmt = sa.select([player]).where(accounts.c.id == account_id)

        result = conn.execute(stmt).first()
        if result is not None:
            return _parse_row(result)
