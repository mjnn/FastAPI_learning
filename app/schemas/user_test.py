from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated


class UserBase(BaseModel):
    username: str
    email: EmailStr

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