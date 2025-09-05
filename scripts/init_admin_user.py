#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本 - 创建管理员用户和角色
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.database import engine, SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.auth.password import get_password_hash

def create_admin_role(db: Session) -> Role:
    """
    创建管理员角色
    """
    # 检查是否已存在管理员角色
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if admin_role:
        print("管理员角色已存在")
        return admin_role
    
    # 创建管理员角色
    admin_role = Role(
        name="admin",
        display_name="系统管理员",
        description="系统管理员，拥有所有权限",
        is_active=True
    )
    
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)
    print(f"创建管理员角色成功: {admin_role.display_name}")
    return admin_role

def create_admin_user(db: Session, username: str = "wangcw", password: str = "Lunz2017", email: str = "rubygreat@msn.com") -> User:
    """
    创建管理员用户
    """
    # 检查是否已存在管理员用户
    admin_user = db.query(User).filter(User.username == username).first()
    if admin_user:
        print(f"用户 {username} 已存在")
        return admin_user
    
    # 创建管理员用户
    hashed_password = get_password_hash(password)
    admin_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name="系统管理员",
        is_active=True,
        is_superuser=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"创建管理员用户成功: {admin_user.username}")
    return admin_user

def assign_admin_role(db: Session, user: User, role: Role) -> UserRole:
    """
    为用户分配管理员角色
    """
    # 检查是否已分配角色
    user_role = db.query(UserRole).filter(
        UserRole.user_id == user.id,
        UserRole.role_id == role.id
    ).first()
    
    if user_role:
        print(f"用户 {user.username} 已拥有 {role.display_name} 角色")
        return user_role
    
    # 分配角色
    user_role = UserRole(
        user_id=user.id,
        role_id=role.id,
        assigned_at=datetime.now()
    )
    
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    print(f"为用户 {user.username} 分配 {role.display_name} 角色成功")
    return user_role

def init_admin_data():
    """
    初始化管理员数据
    """
    print("开始初始化管理员数据...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 1. 创建管理员角色
        admin_role = create_admin_role(db)
        
        # 2. 创建管理员用户
        admin_user = create_admin_user(db)
        
        # 3. 为管理员用户分配角色
        assign_admin_role(db, admin_user, admin_role)
        
        print("\n管理员数据初始化完成!")
        print(f"管理员用户名: {admin_user.username}")
        print(f"管理员邮箱: {admin_user.email}")
        print("默认密码: admin123")
        print("\n请及时修改默认密码!")
        
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_admin_data()