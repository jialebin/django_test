from django_redis import get_redis_connection
from rest_framework import serializers
import re
from rest_framework_jwt.settings import api_settings


from .models import User
from celery_tasks.emali.tasks import send_activation_email

import logging
logger = logging.getLogger('django')


class CreateUserSerializer(serializers.ModelSerializer):

    # password2 = serializers.CharField(label='确认密码', write_only=True)
    allow = serializers.BooleanField(label="同意协议", write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    # image_code_text = serializers.CharField(label='图片验证码value', read_only=True)
    # image_code_id = serializers.CharField(label='图片验证码key', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'allow', 'token')

    def validate_allow(self, value):
        if value != True:
            raise serializers.ValidationError('未同意协议')
        return value

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value
        pass

    def create(self, validated_data):
        del validated_data['allow']

        user = super().create(validated_data)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        send_activation_email(validated_data['email'], token)
        return user


class LogInByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify = serializers.CharField(max_length=6)

    def validate(self, attrs):
        verify = attrs['verify']
        email = attrs['email']

        redis_conn = get_redis_connection('verify_codes')

        redis_verify = redis_conn.get('login_email_%s' % email)
        if redis_verify is None:
            raise serializers.ValidationError('邮箱错误')
        elif redis_verify.decode() != verify.upper():
            raise serializers.ValidationError('验证码错误')
        return attrs
