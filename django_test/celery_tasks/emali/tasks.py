from celery_tasks.main import celery_app
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from email.mime.image import MIMEImage


# @celery_app.task(name='send_verify_email')
# def send_verify_email(to_email, image_rb):
#     '''
#     发送登录邮件
#     :param to_email: 收件人邮箱
#     :param verify_url: 验证链接
#     :return: None
#     '''
#     subject = '登录验证邮件'
#
#     html = '''
#          <!DOCTYPE html>
#          <html lang="en">
#          <head>
#              <meta charset="UTF-8">
#              <title>Title</title>
#          </head>
#          <body>
#          <p>尊敬的用户您好！</p>
#          <p>您正在登录  网站登录验证码为(该图片无法显示请查看附件)：</p>
#          <img src="cid:test_cid"/>
#          </body>
#          </html>
#          '''
#
#     msg = mail.EmailMessage(subject, html, '验证邮箱', [to_email])
#     msg.content_subtype = 'html'
#     msg.encoding = 'utf-8'
#     msg_image = MIMEImage(image_rb)
#     msg_image.add_header('Content-ID', '<' + '图片验证码' + '>')
#     msg.attach(msg_image)
#     msg.send()


@celery_app.task(name='send_verify_email')
def send_verify_email(to_email, verify_str):
    '''
    发送验证邮箱邮件
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    '''
    subject = '登录验证码'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用</p>' \
                   '<p>您的登录验证码是</p>' \
                   '<p>%s</p>' % (verify_str,)

    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)


@celery_app.task(name='send_verify_email')
def send_activation_email(to_email, verify_url):
    '''
    发送验证邮箱邮件
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    '''

    subject = '***用户激活邮箱'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您××××。</p>' \
                   '<p>点击一下链接进行激活</p>' \
                   '<p><a href="%s">%s<a></p>' % (verify_url, verify_url)

    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)