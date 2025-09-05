from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

class PermissionService:
    """权限服务类"""
    
    @staticmethod
    def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
        """获取权限列表"""
        return db.query(Permission).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_permission_by_id(db: Session, permission_id: int) -> Optional[Permission]:
        """根据ID获取权限"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
        """根据名称获取权限"""
        return db.query(Permission).filter(Permission.name == name).first()
    
    @staticmethod
    def create_permission(db: Session, permission_create: PermissionCreate) -> Permission:
        """创建权限"""
        # 检查权限名称是否已存在
        existing_permission = PermissionService.get_permission_by_name(db, permission_create.name)
        if existing_permission:
            raise ValueError(f"权限名称 '{permission_create.name}' 已存在")
        
        db_permission = Permission(
            name=permission_create.name,
            display_name=permission_create.display_name,
            description=permission_create.description,
            resource=permission_create.resource,
            action=permission_create.action,
            is_active=permission_create.is_active
        )
        
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    @staticmethod
    def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate) -> Optional[Permission]:
        """更新权限"""
        db_permission = PermissionService.get_permission_by_id(db, permission_id)
        if not db_permission:
            return None
        
        update_data = permission_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)
        
        db.commit()
        db.refresh(db_permission)
        return db_permission
    
    @staticmethod
    def delete_permission(db: Session, permission_id: int) -> bool:
        """删除权限"""
        db_permission = PermissionService.get_permission_by_id(db, permission_id)
        if not db_permission:
            return False
        
        db.delete(db_permission)
        db.commit()
        return True
    
    @staticmethod
    def get_permissions_by_resource(db: Session, resource: str) -> List[Permission]:
        """根据资源获取权限列表"""
        return db.query(Permission).filter(Permission.resource == resource).all()
    
    @staticmethod
    def get_permissions_by_action(db: Session, action: str) -> List[Permission]:
        """根据操作类型获取权限列表"""
        return db.query(Permission).filter(Permission.action == action).all()