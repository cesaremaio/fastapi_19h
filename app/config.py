from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    # jwt
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int

    # import from .env file
    class Config:
        env_file = ".env"
