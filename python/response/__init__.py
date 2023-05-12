from .base import ERR
from .exceptions import BizException
from .generic import R

OK = ERR.register(200, "请求成功")
ERROR = ERR.register(400, "请求错误")
NOT_FOUND = ERR.register(404, "该内容不存在")
COONNECT_ERROR = ERR.register(406, "数据库出错错误")
PARAM_ERROR = ERR.register(401, "请求参数错误")
NOT_LOGIN = ERR.register(403, "用户登录失效")
PERMISSION_REQUIRED = ERR.register(410, "用户角色权限不足")
NOT_SUPER_ADMIN = ERR.register(411, "用户无超级管理员权限")
PROCESS_NOT_FOUND = ERR.register(408, "该Process不存在")
PLATFORM_NOT_FOUND = ERR.register(409, "未连接平台")
INTERNAL_ERROR = ERR.register(500, "服务器内部错误")
