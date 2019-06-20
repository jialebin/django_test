from django_redis import get_redis_connection
from rest_framework import serializers
import re
from rest_framework_jwt.settings import api_settings

from .models import User

import logging
logger = logging.getLogger('django')


class CreateUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(label='确认密码', write_only=True)
    allow = serializers.BooleanField(label="同意协议", write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    image_code_text = serializers.CharField(label='图片验证码value', read_only=True)
    image_code_id = serializers.CharField(label='图片验证码key', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'email', 'password2', 'allow', 'token', 'image_code_text',
                  'image_code_id')

    def validate_allow(self, value):
        if value != True:
            raise serializers.ValidationError('未同意协议')
        return value

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value
        pass

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        image_code_text = attrs.get('image_code_text')
        image_code_id = attrs.get('image_code_id')

        if password != password2:
            raise serializers.ValidationError('两次密码不一致')
        redis_conn = get_redis_connection("verify_codes")
        try:
            image_server_code = redis_conn.get('img_%s' % image_code_id)
        except Exception as e:
            raise serializers.ValidationError('请重试')
        if image_server_code is None:
            raise serializers.ValidationError('验证码过期')
        if image_server_code.decode() != image_code_text.upper():
            raise serializers.ValidationError('验证码错误')
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except Exception as e:
            logger.error(e)
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['allow']
        del validated_data['image_code_text']
        del validated_data['image_code_id']

        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

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
