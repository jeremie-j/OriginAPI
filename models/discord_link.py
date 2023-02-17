from datetime import datetime
from dateutil import tz

import sqlalchemy as sa

from db.session import metadata

discord_link = sa.Table(
    "player",
    metadata,
    sa.Column("uid", sa.BIGINT, nullable=False),
    sa.Column(
        "discord_id",
        sa.BIGINT,
        primary_key=True,
    ),
    sa.Column("platform", sa.String),
    sa.Column("created_at", sa.TIMESTAMP,
              default=lambda: datetime.now(tz=tz.UTC)),
)
