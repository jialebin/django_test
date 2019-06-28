from django.core.files.storage import Storage
import oss2

class OSSStorage(Storage):

    def __init__(self):
        pass

    def _save(self, name, content):
        """
        文件要存储时会自动的调用的方法
        自定义自己的文件保存（实际文件保存逻辑）
        ：:param : 要保存的文件名字
        :param content : 要存储的文件对象，是File类型的对象，需要调用read（）读取出里面的文件内容二进制
        :return: 保存的文件名的实际名称
        """
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
        bucket = oss2.Bucket(auth, endpoint, '<yourBucketName>', connect_timeout=30)
        result = bucket.put_object('<yourObjectName>', b'content of object')
        return result.headers.get()

    def _open(self, name, mode='rb'):
        """
        不涉及打开所以pass
        :return: 这个方法必须要返回一个文件对象。
        """
        pass

    def delete(self, name):
        """
        删除文件
        :param name:
        :return:
        """
        pass

    def exists(self, name):
        """
        判断文件是否存在
        :param name: 文件名
        :return:
        """
        return False

    def listdir(self, path):
        """
        列出指定路径的内容，返回2元组列表; 第一项是目录，第二项是文件。对于无法提供此类列表的存储系统，这将引发NotImplementedError相反的情况。
        :param path:
        :return:
        """
        pass

    def size(self, name):
        """
        返回文件大小
        :param name:
        :return:
        """
        pass

    def url(self, name):
        """
        需要在这个方法中，拼接文件的全路径，用于将来做文件的下载的
        :param name:
        :return: 文件的完整URL
        """
        url = '' + name
        return url
