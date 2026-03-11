from fastapi import FastAPI,Request
from app.routers.v1 import get_post_test
from app.core.config import settings
from app.core.response import success_response, error_response, request_validation_handler
from fastapi.exceptions import RequestValidationError



# 实例化FastAPI
app = FastAPI()

# 注册请求参数的类型验证错误
app.exception_handler(RequestValidationError)(request_validation_handler)

# 注册路由
app.include_router(
    get_post_test.router,
    prefix=settings.API_V1_STR
)

@app.get('/')
def root():
    return success_response('Here is Root!')