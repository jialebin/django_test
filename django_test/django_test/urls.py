"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
# from django.urls.resolvers import RegexURLPattern, RegexURLResolver
from django.urls.resolvers import URLPattern, URLResolver
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('verify/', include('verifications.urls')),
]


def get_all_url(urlparrentens, parent_regex='', is_firt_time=False, url_list=[]):
    if isinstance(urlparrentens, URLPattern):
        regex = urlparrentens._regex.strip('^$')
        url_list.append(((parent_regex + regex), urlparrentens.name))
        return

    if isinstance(urlparrentens, URLResolver):
        regex = urlparrentens._regex.strip('^$')
        if urlparrentens._regex.strip('^$') == 'xadmin/':
            url_list.append((urlparrentens._regex.strip('^$'), 'xadmin'))
        else:
            get_all_url(urlparrentens.url_patterns, parent_regex + regex, url_list=url_list)
        return

    for item in urlparrentens:
        if isinstance(urlparrentens, URLResolver):
            regex = item._regex.strip('^$')
            get_all_url(item, parent_regex + regex, url_list=url_list)

        elif isinstance(urlparrentens, list):
            get_all_url(item, parent_regex, url_list=url_list)

        # else:
        #     url_list.append(((parent_regex+item._regex),  item.name))
    return url_list
    pass


# url_list = get_all_url(urlpatterns, is_firt_time=True)
"""
调用保存所有ＵＲＬ的方法
"""
# for url in url_list:
#     print(url)
# print(len(url_list))
