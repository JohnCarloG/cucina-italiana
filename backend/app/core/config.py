from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user:password@host:3306/cucina"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_exp_days: int = 7
    price_service_fee: float = 1.5

    class Config:
        env_file = ".env"


settings = Settings()
