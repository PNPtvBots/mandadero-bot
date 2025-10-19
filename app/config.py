from pydantic import BaseSettings

class Config(BaseSettings):
    bot_token: str
    db_url: str
    admin_chat_id: str
    
    class Config:
        env_file = ".env"