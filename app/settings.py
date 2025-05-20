from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MongoDsn

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    database_url: str
    databases_user: str
    databases_password: str

config = Config()
