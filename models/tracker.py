from datetime import datetime
from dateutil import tz

import sqlalchemy as sa

from db.session import metadata

tracker = sa.Table(
    "trackers",
    metadata,
    sa.Column(
        "uid",
        sa.BIGINT,
        primary_key=True,
    ),
    sa.Column("legend", sa.String, nullable=False),
    sa.Column("tracker", sa.String, nullable=False),
    sa.Column("value", sa.String, nullable=False),
    sa.Column("created_at", sa.TIMESTAMP,
              default=lambda: datetime.now(tz=tz.UTC)),
)
