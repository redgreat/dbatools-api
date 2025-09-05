from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    """权限基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="权限名称")
    display_name: str = Field(..., min_length=1, max_length=100, description="权限显示名称")
    description: Optional[str] = Field(None, description="权限描述")
    resource: str = Field(..., min_length=1, max_length=100, description="资源名称")
    action: str = Field(..., min_length=1, max_length=50, description="操作类型")
    is_active: bool = Field(True, description="是否激活")

class PermissionCreate(PermissionBase):
    """创建权限请求模型"""
    pass

class PermissionUpdate(BaseModel):
    """更新权限请求模型"""
    display_name: Optional[str] = Field(None, min_length=1, max_length=100, description="权限显示名称")
    description: Optional[str] = Field(None, description="权限描述")
    resource: Optional[str] = Field(None, min_length=1, max_length=100, description="资源名称")
    action: Optional[str] = Field(None, min_length=1, max_length=50, description="操作类型")
    is_active: Optional[bool] = Field(None, description="是否激活")

class PermissionResponse(PermissionBase):
    """权限响应模型"""
    id: int = Field(..., description="权限ID")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True