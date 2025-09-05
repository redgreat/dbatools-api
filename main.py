from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import auth, users, roles, permissions
from app.database import engine
from app.models import Base
import logging
import uvicorn

# 配置日志，屏蔽uvicorn的access日志中的特定404错误
class CustomUvicornFilter(logging.Filter):
    """自定义日志过滤器，屏蔽Vite相关的404请求"""
    def filter(self, record):
        # 屏蔽包含@vite、node_modules、src等路径的404日志
        if hasattr(record, 'getMessage'):
            message = record.getMessage()
            if ('404 Not Found' in message and 
                ('/@vite/' in message or '/node_modules/' in message or '/src/' in message)):
                return False
        return True

# 应用过滤器到uvicorn的access日志
logging.getLogger('uvicorn.access').addFilter(CustomUvicornFilter())

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DBA Tools API",
    description="数据库管理工具后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由来处理Vite相关请求，避免404错误
@app.get("/@vite/{path:path}")
async def handle_vite_requests(path: str):
    """处理Vite开发服务器相关请求"""
    return JSONResponse(status_code=404, content={"detail": "Vite resource not found"})

@app.get("/node_modules/{path:path}")
async def handle_node_modules_requests(path: str):
    """处理node_modules相关请求"""
    return JSONResponse(status_code=404, content={"detail": "Node modules resource not found"})

@app.get("/src/{path:path}")
async def handle_src_requests(path: str):
    """处理src相关请求"""
    return JSONResponse(status_code=404, content={"detail": "Source resource not found"})

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(roles.router, prefix="/api/roles", tags=["角色管理"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["权限管理"])

@app.get("/")
async def root():
    """根路径健康检查接口"""
    return {"message": "DBA Tools API is running"}

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    uvicorn.run(app, host=settings.host, port=settings.port)