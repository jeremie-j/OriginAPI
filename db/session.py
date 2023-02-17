from sqlalchemy import create_engine, MetaData

from config.settings import settings


engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=1,
)

metadata = MetaData()
