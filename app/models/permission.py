from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Permission(BaseModel):
    """权限模型"""
    __tablename__ = "permissions"
    
    name = Column(String(50), unique=True, nullable=False, index=True, comment="权限名称")
    display_name = Column(String(100), nullable=False, comment="权限显示名称")
    description = Column(Text, comment="权限描述")
    resource = Column(String(100), nullable=False, comment="资源名称")
    action = Column(String(50), nullable=False, comment="操作类型")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    def __repr__(self):
        return f"<Permission(name='{self.name}', resource='{self.resource}', action='{self.action}')>"