from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

load_dotenv() # Load from .env file

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables. 
    Values are defined in the `.env` file.

    Attributes:
        POSTGRES_DB (str): Name of the PostgreSQL database.
        POSTGRES_USER (str): Database username.
        POSTGRES_PASSWORD (str): Database password. 
        POSTGRES_HOST (str): Hostname of the datbase.
        POSTGRES_PORT (int): Port number for PostgreSQL (default to 5432).
    """
    
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost" # Default fallback 
    POSTGRES_PORT: int = 5432 # Default PostgreSQL port 
    database_url: str
    
    model_config = { # Configuration for reading environment variables from a .env file and allowing extra env variables
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }
    
    @property
    def database_url(self) -> str:
        """
        Build a full PostgreSQL connection URL.

        Returns:
            str: A SQLAlchemy compatible database URL.
        """
        return (
            #f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
@lru_cache()
def get_settings() -> Settings:
    """
    Ensures the Settings config is loaded only once across the application.

    Returns:
        Settings: An instance of the Settings class
    """
    return Settings()

settings = get_settings() # Easy to import 