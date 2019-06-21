from celery_tasks.main import celery_app
from django.conf import settings

from .yuntongxun.sms import CCP
from .constants import SMS_CODE_REDIS_EXPIRES


@celery_app.task(name='send_sms')
def send_verify_sms(mobile, sms_code):
    ccp = CCP()
    ccp.send_template_sms(mobile, [sms_code, SMS_CODE_REDIS_EXPIRES // 60], 1)
