#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证管理员用户和角色是否创建成功
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.auth.password import verify_password

def verify_admin_data():
    """
    验证管理员数据
    """
    print("开始验证管理员数据...")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 1. 验证管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("❌ 管理员用户不存在")
            return False
        
        print(f"✅ 管理员用户存在: {admin_user.username}")
        print(f"   - 邮箱: {admin_user.email}")
        print(f"   - 全名: {admin_user.full_name}")
        print(f"   - 是否激活: {admin_user.is_active}")
        print(f"   - 是否超级用户: {admin_user.is_superuser}")
        print(f"   - 创建时间: {admin_user.created_at}")
        
        # 2. 验证密码
        if verify_password("admin123", admin_user.hashed_password):
            print("✅ 默认密码验证成功")
        else:
            print("❌ 默认密码验证失败")
        
        # 3. 验证管理员角色
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("❌ 管理员角色不存在")
            return False
        
        print(f"✅ 管理员角色存在: {admin_role.name}")
        print(f"   - 显示名称: {admin_role.display_name}")
        print(f"   - 描述: {admin_role.description}")
        print(f"   - 是否激活: {admin_role.is_active}")
        print(f"   - 创建时间: {admin_role.created_at}")
        
        # 4. 验证用户角色关联
        user_role = db.query(UserRole).filter(
            UserRole.user_id == admin_user.id,
            UserRole.role_id == admin_role.id
        ).first()
        
        if not user_role:
            print("❌ 用户角色关联不存在")
            return False
        
        print(f"✅ 用户角色关联存在")
        print(f"   - 分配时间: {user_role.assigned_at}")
        
        # 5. 统计信息
        total_users = db.query(User).count()
        total_roles = db.query(Role).count()
        total_user_roles = db.query(UserRole).count()
        
        print("\n📊 数据库统计:")
        print(f"   - 总用户数: {total_users}")
        print(f"   - 总角色数: {total_roles}")
        print(f"   - 总用户角色关联数: {total_user_roles}")
        
        print("\n🎉 管理员数据验证完成，一切正常!")
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_admin_data()