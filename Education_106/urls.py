"""Education_106 URL Configuration

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
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt#去除token验证
from django.views.static import serve


import xadmin

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView
from apps.operations.views import IndexView
from Education_106.settings import MEDIA_ROOT

from apps.courses import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    #一级单页面url
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('d_login/', DynamicLoginView.as_view(), name="d_login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),

    #上传文件
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    #机构
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),

    #课程
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),

    #行为
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),

    #用户
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

    #富文本编辑器
    url(r'^ueditor/',include('DjangoUeditor.urls')),

    #支付宝付款
    path('purchase/<course_id>/', views.purchase),
    path('show_msg/', views.show_msg),

]

