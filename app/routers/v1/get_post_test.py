from fastapi import APIRouter,Body
from app.core.response import success_response, error_response, BaseResponseModel, ErrorResponseModel
from app.schemas.get_post_test import two_numbers
from typing import Annotated

# 创建路由实例
router = APIRouter(
    prefix="/get_post_test",
    tags=["get_post_test"]
)

@router.get("/", response_model=BaseResponseModel)
async def just_get():
    """
    这是一个没有任何参数的Get请求
    """
    return success_response('这是一个没有任何参数的Get请求')


@router.get("/path_param/{num1}/{num2}", response_model=BaseResponseModel)
async def path_param(num1: int = None, num2: int = None):
    """
    这是一个路径参数请求
    """
    result = num1 + num2
    return success_response(f'{num1}+{num2}={result}')

@router.get("/query_param", response_model=BaseResponseModel)
async def query_param(num1: int, num2: int):
    """
    这是一个查询参数请求
    """
    result = num1 + num2
    return success_response(f'{num1}+{num2}={result}')


@router.post("/body_param", response_model=BaseResponseModel)
async def body_param(
        numbers: Annotated[
            two_numbers,
            Body(
                openapi_examples = {
                '1+2':{
                    'summary':'1+2示例',
                    'description':'展示1+2请求输入',
                    'value':{
                        'num1': 1,
                        'num2': 2
                    }
                },
                '2+3':{
                    'summary':'2+3示例',
                    'description':'展示2+3请求输入',
                    'value':{
                        'num1': 2,
                        'num2': 3
                    }
                },
            }
            )
        ]):
    """
    这是一个带请求体的请求
    """
    num1=numbers.num1
    num2=numbers.num2
    result = num1 + num2
    return success_response(f'{num1}+{num2}={result}')
