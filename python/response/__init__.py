from .exceptions import ApiException
from .generic import R, ErrResponse

OK = ErrResponse.register(200, "请求成功")
ERROR = ErrResponse.register(400, "请求错误")
NOT_FOUND = ErrResponse.register(404, "该内容不存在")
COONNECT_ERROR = ErrResponse.register(406, "数据库出错错误")
PARAM_ERROR = ErrResponse.register(401, "请求参数错误")
NOT_LOGIN = ErrResponse.register(403, "用户登录失效")
PERMISSION_REQUIRED = ErrResponse.register(410, "用户角色权限不足")
NOT_SUPER_ADMIN = ErrResponse.register(411, "用户无超级管理员权限")
INTERNAL_ERROR = ErrResponse.register(500, "服务器内部错误")
