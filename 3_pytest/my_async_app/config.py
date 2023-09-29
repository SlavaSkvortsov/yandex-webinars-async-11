from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


settings = Settings()
