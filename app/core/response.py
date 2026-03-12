from typing import Generic, TypeVar, Optional, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy.exc import IntegrityError

# 泛型类型定义
T = TypeVar("T")


# -------------------------- 重构响应模型 --------------------------
class BaseResponseModel(GenericModel, Generic[T]):
    """基础响应模型（无code字段，code作为HTTP状态码）"""
    message: str = Field(description="返回消息")
    data: Optional[T] = Field(None, description="返回数据")


class SuccessResponseModel(BaseResponseModel[T]):
    """成功响应模型"""
    message: str = Field("success", description="成功消息")


class ErrorResponseModel(BaseModel):
    """错误响应模型（含错误详情）"""
    message: str = Field("error", description="错误消息")
    errors: Optional[Any] = Field(None, description="错误详情")


# -------------------------- 快捷响应函数 --------------------------
def success_response(
        data: Optional[Any] = None,
        message: str = "success",
        http_code: int = 200  # 这里的http_code就是真正的HTTP状态码
):
    """成功响应：直接返回JSONResponse，设置HTTP状态码"""
    response_data = SuccessResponseModel(message=message, data=data).model_dump()
    return JSONResponse(
        status_code=http_code,  # 映射为HTTP状态码
        content=response_data
    )


def error_response(
        message: str = "error",
        errors: Optional[Any] = None,
        http_code: int = 400  # 错误的HTTP状态码（如404、422、500等）
):
    """错误响应：直接返回JSONResponse，设置HTTP状态码"""
    response_data = ErrorResponseModel(message=message, errors=errors).model_dump()
    return JSONResponse(
        status_code=http_code,  # 映射为HTTP状态码
        content=response_data
    )


# -------------------------- 异常处理器改造 --------------------------
async def request_validation_handler(request: Request, exc: RequestValidationError):
    """处理请求参数验证错误（HTTP 422）"""
    # 格式化验证错误信息
    custom_errors = []
    for error in exc.errors():
        custom_errors.append({
            "field": ".".join(error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    # 返回422 HTTP状态码 + 自定义错误格式
    return error_response(
        message="参数验证失败",
        errors=custom_errors,
        http_code=422  # 符合HTTP规范的422状态码
    )


async def sqlmodel_validation_handler(request: Request, exc: IntegrityError):
    """处理数据库约束错误（HTTP 400）"""
    # 解析异常信息
    if "UNIQUE constraint failed" in str(exc):
        if "username" in str(exc):
            message = "用户名已存在"
        elif "email" in str(exc):
            message = "邮箱已被注册"
        else:
            message = "数据重复，无法创建/更新"
    else:
        message = "数据库约束错误，请检查输入数据"

    # 返回400 HTTP状态码 + 错误详情
    return error_response(
        message=message,
        errors=str(exc.orig),
        http_code=400  # 客户端参数错误对应400
    )


# -------------------------- 示例接口使用 --------------------------
from fastapi import FastAPI

app = FastAPI()

# 注册异常处理器
app.add_exception_handler(RequestValidationError, request_validation_handler)
app.add_exception_handler(IntegrityError, sqlmodel_validation_handler)


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id == 0:
        # 模拟错误：返回404 HTTP状态码
        return error_response(
            message="用户不存在",
            errors=f"用户ID {user_id} 未找到",
            http_code=404
        )
    # 模拟成功：返回200 HTTP状态码
    return success_response(
        data={"user_id": user_id, "username": "test_user"},
        message="查询成功",
        http_code=200
    )


@app.post("/users/")
async def create_user(username: str, email: str):
    # 模拟成功创建：返回201 Created状态码（符合REST规范）
    return success_response(
        data={"username": username, "email": email},
        message="用户创建成功",
        http_code=201
    )