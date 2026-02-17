"""
AgentMem 客户端异常定义
"""


class AgentMemException(Exception):
    """AgentMem 基础异常"""
    pass


class AuthenticationError(AgentMemException):
    """认证失败异常"""
    pass


class NotFoundError(AgentMemException):
    """资源不存在异常"""
    pass


class ValidationError(AgentMemException):
    """数据验证失败异常"""
    pass


class ConnectionError(AgentMemException):
    """连接异常"""
    pass


class ServerError(AgentMemException):
    """服务器错误异常"""
    pass
