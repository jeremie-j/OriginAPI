from pydantic import BaseSettings


class Config(BaseSettings):
    origin_email: str
    origin_pass: str
    database_url: str

    class Config:
        env_file = '.env'


settings = Config()
