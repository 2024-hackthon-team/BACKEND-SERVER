import typing as T
from functools import lru_cache

from pydantic import ConfigDict, Field, MySQLDsn
from pydantic_settings import BaseSettings


@lru_cache
def _build_mysql_host(
    mysql_user: str,
    mysql_password: str,
    mysql_host: str,
    mysql_port: int,
    path: str | None = None,
    query: str | None = None,
) -> MySQLDsn:
    return MySQLDsn.build(
        scheme="mysql+pymysql",
        username=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        path=path,
        query=query,
    )


class Config(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    deploy_env: T.Literal["development", "production", "testing"]

    # Database
    mysql_host: str = Field(..., exclude=True, repr=False)
    mysql_port: int = Field(..., exclude=True, repr=False)
    mysql_user: str = Field("root", exclude=True, repr=False)
    mysql_password: str = Field(
        ..., validation_alias="MYSQL_ROOT_PASSWORD", exclude=True, repr=False
    )
    mysql_database: str = Field(..., exclude=True, repr=False)

    @property
    def mysql_url(self) -> MySQLDsn:
        return _build_mysql_host(
            mysql_user=self.mysql_user,
            mysql_password=self.mysql_password,
            mysql_host=self.mysql_host,
            mysql_port=self.mysql_port,
            path=self.mysql_database,
            query="charset=utf8",
        )


# TODO: Change env_file depending on the environment
env_file = ".env"
config = Config(_env_file=env_file)
