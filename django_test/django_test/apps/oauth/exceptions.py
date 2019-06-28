class QQAPIException(Exception):
    """
    自定义QQ登录的异常
    只捕获异常，不处理异常
    """
    pass


class WeChatAPIException(Exception):
    """
    自定义微信登录的异常
    只捕获异常，不处理异常
    """
    pass
