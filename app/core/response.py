from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
# 定义泛型类型
T = TypeVar("T")

# GenericModel是泛型pydantic模型
class ResponseModel(GenericModel, Generic[T]):
    """统一返回格式模型"""
    # 状态码
    code: int = Field(200, description="状态码，200表示成功")
    # 返回消息
    message: str = Field("success", description="返回消息")
    # 数据允许是T(泛型类型)或者None
    data: Optional[T] = Field(None, description="返回数据")


class ErrorResponseModel(BaseModel):
    """错误返回格式模型"""
    code: int = Field(400, description="错误状态码")
    message: str = Field("error", description="错误消息")
    data: Optional[Any] = Field(None, description="错误详情")


# 快捷返回函数
def success_response(data: Optional[Any] = None, message: str = "success", code: int = 200):
    """成功响应"""
    return ResponseModel(code=code, message=message, data=data)


def error_response(message: str = "error", data: Optional[Any] = None, code: int = 400):
    """错误响应"""
    return ErrorResponseModel(code=code, message=message, data=data)


async def request_validation_handler(request: Request, exc: RequestValidationError):
    """
    处理所有请求参数/请求体的类型验证错误
    :param request: 请求对象
    :param exc: 验证错误异常对象
    """
    # 1. 提取原始错误信息（FastAPI 自带的详细错误）
    raw_errors = exc.errors()
    # 2. 自定义返回格式（更友好的提示）
    custom_errors = []
    for error in raw_errors:
        custom_errors.append({
            "field": ".".join(error["loc"]),  # 错误字段（如 body.name、query.page）
            "message": error["msg"],  # 错误提示（如 "value is not a valid integer"）
            "type": error["type"]  # 错误类型（如 "type_error.integer"）
        })

    # 3. 返回自定义的 JSON 响应
    return JSONResponse(
        status_code=422,  # 保持 422 Unprocessable Entity 状态码（符合 HTTP 规范）
        content={
            "code": 400,
            "msg": "参数验证失败",
            "errors": custom_errors
        }
    )
