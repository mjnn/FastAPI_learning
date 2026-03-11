from fastapi import FastAPI
from pydantic import BaseModel

class two_numbers(BaseModel):
    """包含两个整数的模型"""
    num1:int = None
    num2:int = None