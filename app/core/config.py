from pydantic_settings import BaseSettings

class settings(BaseSettings):
    # 路由初始地址
    API_V1_STR:str = '/api/v1'
    # 是否开启Debug模式
    DEBUG:bool = True

settings = settings()