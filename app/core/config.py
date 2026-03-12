from pydantic_settings import BaseSettings
import os

class settings(BaseSettings):
    # 路由初始地址
    API_V1_STR : str = '/api/v1'
    # 是否开启Debug模式
    DEBUG:bool = True


    SQLITE_URL:str = "sqlite:///database.db"
    CHECK_SAME_THREAD : bool = False

settings = settings()


