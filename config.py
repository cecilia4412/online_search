from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TAVILY_API_KEY: str = ""
    TENCENT_SECRET_ID: str = ""
    TENCENT_SECRET_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
