from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializers,BadData

from . import contants
# Create your models here.


class User(AbstractUser):
    """
    用户模型类
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='用户验证邮箱')
    email = models.EmailField(unique=True, verbose_name='用户邮箱')
    head_portrait = models.ImageField(null=True, verbose_name='头像')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_activation_email_url(self):
        # 生成验证邮箱的激活url
        serializer = Serializers(settings.SECRET_KEY,expires_in=contants.VERIFY_EMAIL_TOKEN_EXPIRES)
        data = {'user_id': self.id, 'email': self.email}
        token = serializer.dumps(data).decode()
        verify_url = 'http://www.lovelogging.com/email_activation.html?token=' + token
        return verify_url

    @staticmethod
    def check_activation_email_token(token):
        '''检查验证邮件的token'''

        serializer = Serializers(settings.SECRET_KEY, expires_in=contants.VERIFY_EMAIL_TOKEN_EXPIRES)

        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            email = data.get('email')
            user_id = data.get('user_id')
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user
