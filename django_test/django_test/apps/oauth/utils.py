from urllib.parse import urlencode
from urllib.parse import parse_qs
from urllib.request import urlopen
from django.conf import settings
import json

from .exceptions import QQAPIException

import logging
logger = logging.getLogger('django')


class OAuthQQ(object):
    """
    QQ登录的工具类：封装了QQ登录的部分过程
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        """
        初始化参数
        :param client_id: app_id
        :param client_secret: app_key
        :param redirect_uri: 回调地址
        :param state:
        """
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE

    def get_login_url(self):
        """
        获取QQ登录页面
        :return: QQ登录页面的URL
        """

        login_url = 'https://graph.qq.com/oauth2.0/authorize?'

        # 参数
        params = {
            'response_type': 'code',  # 授权类型，此值滚定为‘code’
            'client_id': self.client_id,  # 申请QQ登录成功后，分配给应用的appid
            'redirect_uri': self.redirect_uri,
            'state': self.state,  # client端的状态值--一般写text--登录之前打开的网页
            'scope': 'get_user_info'  # 请求用户授权时向用户显示的可进行授权的列表
        }
        query_params = urlencode(params)
        login_url += query_params
        return login_url

    def get_access_token(self, code):
        """
        通过code值获取access_token
        :param code: authorization code
        :return: access_token
        """

        url = 'https://graph.qq.com/oauth2.0/token?'

        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        query_params = urlencode(params)
        url += query_params
        try:
            response_data = urlopen(url).read()
            response_str = response_data.decode()
            response_dict = parse_qs(response_str)
            access_token = response_dict.get('access_token')[0]
        except Exception as e:
            logging.info(e)
            raise QQAPIException('QQ登录获取access_token失败')
        return access_token

    def get_open_id(self, access_token):
        """
        使用access_token获取openid
        :param access_token: 通过code 获取到的access_token
        :return: openid
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=%s' % access_token
        response_str = ''
        try:
            response_data = urlopen(url).read()
            response_str = response_data.decode()
            response_dict = json.loads(response_str[10:-4])

            open_id = response_dict.get('openid')
        except Exception as e:
            err_data = parse_qs(response_str)
            logger.error(e)
            raise QQAPIException('code=%s msg=%s'%(err_data.get('code'),err_data.get('msg')))
        return open_id
