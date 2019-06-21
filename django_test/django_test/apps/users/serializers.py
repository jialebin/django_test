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
    sms_code = serializers.CharField(label='短信验证码')
    # image_code_text = serializers.CharField(label='图片验证码value', read_only=True)
    # image_code_id = serializers.CharField(label='图片验证码key', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'allow', 'mobile')

    def validate_allow(self, value):
        if value != True:
            raise serializers.ValidationError('未同意协议')
        return value

    def validate(self, attrs):
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']

        redis_conn = get_redis_connection('verify_codes')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        if redis_sms_code is None:
            raise serializers.ValidationError('验证码过期')
        if str(redis_sms_code.decode()) != sms_code:
            raise serializers.ValidationError('验证码错误')
        return attrs

    def create(self, validated_data):
        del validated_data['allow']

        user = super().create(validated_data)

        activation_url = user.generate_activation_email_url()
        send_activation_email.delay(validated_data['email'], activation_url)
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
