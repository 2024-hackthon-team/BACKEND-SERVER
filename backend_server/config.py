import typing as T

from pydantic import MySQLDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    deploy_env: T.Literal["development", "production", "testing"]
    mysql_host: MySQLDsn


# TODO: Change env_file depending on the environment
env_file = ".env"
config = Config(_env_file=env_file)
