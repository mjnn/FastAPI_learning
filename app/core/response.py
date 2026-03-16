from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

# 泛型类型定义
T = TypeVar("T")


class ResponseModel(GenericModel, Generic[T]):
    """基础响应模型（无code字段，code作为HTTP状态码）"""
    message: str = Field('success', description="返回消息")
    data: Optional[T] = Field(None, description="返回数据")


