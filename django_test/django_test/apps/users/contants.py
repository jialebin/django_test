import datetime
# utils中的自定义认证后台有限时间
login_time = datetime.datetime.now()
lost_time = login_time + datetime.timedelta(hours=+12)
expires_at = lost_time.strftime('%Y-%m-%d %H:%M:%S')

# 邮箱登录验证码有效期 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 邮件激活链接有效期为1天
VERIFY_EMAIL_TOKEN_EXPIRES = 60 * 60 * 12
