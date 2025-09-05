from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.permission import PermissionResponse, PermissionCreate, PermissionUpdate
from app.models.user import User
from app.services.permission_service import PermissionService
from app.services.user_service import UserService
from app.auth.jwt import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[PermissionResponse])
async def get_permissions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取权限列表"""
    permissions = PermissionService.get_permissions(db, skip=skip, limit=limit)
    
    return [
        PermissionResponse(
            id=permission.id,
            name=permission.name,
            display_name=permission.display_name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at
        )
        for permission in permissions
    ]

@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取指定权限信息"""
    permission = PermissionService.get_permission_by_id(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    return PermissionResponse(
        id=permission.id,
        name=permission.name,
        display_name=permission.display_name,
        description=permission.description,
        resource=permission.resource,
        action=permission.action,
        is_active=permission.is_active,
        created_at=permission.created_at
    )

@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_create: PermissionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建权限（需要管理员权限）"""
    # 检查权限
    user_roles = UserService.get_user_roles(db, current_user.id)
    role_names = [role.name for role in user_roles]
    
    if "admin" not in role_names and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        permission = PermissionService.create_permission(db, permission_create)
        
        return PermissionResponse(
            id=permission.id,
            name=permission.name,
            display_name=permission.display_name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新权限信息（需要管理员权限）"""
    # 检查权限
    user_roles = UserService.get_user_roles(db, current_user.id)
    role_names = [role.name for role in user_roles]
    
    if "admin" not in role_names and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    permission = PermissionService.update_permission(db, permission_id, permission_update)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    return PermissionResponse(
        id=permission.id,
        name=permission.name,
        display_name=permission.display_name,
        description=permission.description,
        resource=permission.resource,
        action=permission.action,
        is_active=permission.is_active,
        created_at=permission.created_at
    )

@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除权限（需要管理员权限）"""
    # 检查权限
    user_roles = UserService.get_user_roles(db, current_user.id)
    role_names = [role.name for role in user_roles]
    
    if "admin" not in role_names and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    success = PermissionService.delete_permission(db, permission_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    return {"message": "权限删除成功"}

@router.get("/resource/{resource}", response_model=List[PermissionResponse])
async def get_permissions_by_resource(
    resource: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """根据资源获取权限列表"""
    permissions = PermissionService.get_permissions_by_resource(db, resource)
    
    return [
        PermissionResponse(
            id=permission.id,
            name=permission.name,
            display_name=permission.display_name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at
        )
        for permission in permissions
    ]