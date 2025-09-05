# 修复数据库权限的PowerShell脚本
# 用于解决PostgreSQL权限问题

param(
    [string]$DbHost = "124.70.167.242",
    [string]$Port = "5432",
    [string]$Database = "dbatools",
    [string]$AdminUser = "root",
    [string]$TargetUser = "user_dba"
)

Write-Host "开始修复数据库权限..." -ForegroundColor Green

# 检查psql是否可用
try {
    $psqlVersion = psql --version
    Write-Host "找到PostgreSQL客户端: $psqlVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到psql命令，请确保PostgreSQL客户端已安装并在PATH中" -ForegroundColor Red
    exit 1
}

# 构建连接字符串
$connectionString = "postgresql://$AdminUser@$DbHost`:$Port/$Database"

Write-Host "连接信息:" -ForegroundColor Yellow
Write-Host "  主机: $DbHost" -ForegroundColor Yellow
Write-Host "  端口: $Port" -ForegroundColor Yellow
Write-Host "  数据库: $Database" -ForegroundColor Yellow
Write-Host "  管理员用户: $AdminUser" -ForegroundColor Yellow
Write-Host "  目标用户: $TargetUser" -ForegroundColor Yellow
Write-Host ""

# 提示输入密码
Write-Host "请输入PostgreSQL管理员密码:" -ForegroundColor Cyan

# 执行权限修复脚本
try {
    $scriptPath = Join-Path $PSScriptRoot "fix_database_permissions.sql"
    
    if (-not (Test-Path $scriptPath)) {
        Write-Host "错误: 找不到SQL脚本文件 $scriptPath" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "执行权限修复脚本..." -ForegroundColor Green
    psql -h $DbHost -p $Port -U $AdminUser -d $Database -f $scriptPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "权限修复完成!" -ForegroundColor Green
        Write-Host "现在可以重新运行 'python main.py' 来初始化数据库表" -ForegroundColor Green
    } else {
        Write-Host "权限修复失败，请检查错误信息" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "执行过程中发生错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "脚本执行完成" -ForegroundColor Green