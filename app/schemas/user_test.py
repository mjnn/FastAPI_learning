from pydantic import BaseModel, Field, EmailStr, field_validator,ConfigDict
from typing import Annotated, Literal


class UserBase(BaseModel):
    username: str = Field(
        ...,  # 必填字段
        min_length=1, # 最小长度1位
        max_length=50, # 最大长50
        description="用户名 长度1-50位"
    )
    email: EmailStr = Field(
        ...,
        description="用户邮箱"
    )

class UserForCreate(UserBase):
    password: str = Field(
        ...,  # 必填字段
        min_length=8,  # 最小长度8位
        max_length=128,  # 最大长度128位
        description="密码需包含大小写字母、数字和特殊字符，长度8-128位"
    )

    @field_validator('password')
    def validate_password_strength(cls, v: str) -> str:
        """
        校验密码强度：
        - 至少包含1个大写字母
        - 至少包含1个小写字母
        - 至少包含1个数字
        - 至少包含1个特殊字符（!@#$%^&*()_+-=[]{}|;:,.<>?）
        """
        import re

        # 定义密码强度正则
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]).+$'

        if not re.match(pattern, v):
            raise ValueError(
                "密码强度不足：需包含大小写字母、数字和特殊字符（!@#$%^&*()_+-=[]{}|;:,.<>?）"
            )

        return v

class UserForUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(
        None,
        min_length=1, # 最小长度1位
        max_length=50, # 最大长50
        description="用户名 长度1-50位"
    )
    email: EmailStr = Field(
        None,
        description=""
    )
    password: str = Field(
        None,
        min_length=8,  # 最小长度8位
        max_length=128,  # 最大长度128位
        description="密码需包含大小写字母、数字和特殊字符，长度8-128位"
    )
    is_active: bool = Field(
        None,
        description="是否启用"
    )

    @field_validator('password')
    def validate_password_strength(cls, v: str) -> str:
        """
        校验密码强度：
        - 至少包含1个大写字母
        - 至少包含1个小写字母
        - 至少包含1个数字
        - 至少包含1个特殊字符（!@#$%^&*()_+-=[]{}|;:,.<>?）
        """
        import re
        # 定义密码强度正则
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]).+$'
        if not re.match(pattern, v):
            raise ValueError(
                "密码强度不足：需包含大小写字母、数字和特殊字符（!@#$%^&*()_+-=[]{}|;:,.<>?）"
            )
        return v




query_field_restrict = Literal['username', 'email', 'userid']
class db_user_query(BaseModel):
    query_field : query_field_restrict = 'username'
    query_value : str