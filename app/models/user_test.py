from typing import Annotated, Optional
from sqlmodel import SQLModel,Field
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class DbUserTable(SQLModel, table=True):
    userid: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="用户唯一标识"
    )
    username: str = Field(
        ...,  # 表示必填，不能为 None
        index=True,  # 添加索引提升查询效率
        unique=True,  # 用户名唯一
        max_length=50,  # 限制长度
        description="用户名（唯一）"
    )
    hashed_password: str = Field(
        ...,
        min_length=8,  # 密码哈希值最小长度
        description="密码哈希值"
    )
    email: EmailStr = Field(
        ...,
        unique=True,  # 邮箱唯一
        index=True,
        description="用户邮箱（唯一）"
    )
    is_active: bool = Field(
        default=True,
        description="是否启用（False 表示禁用）"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="创建时间（UTC）"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="更新时间（UTC）"
    )
