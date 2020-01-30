from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from  apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView
from  apps.users.views import MyCourseView, MyFavCourseView, MyMessageView, MyOrderView, MyFavTeacherView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    #头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),
    #修改密码
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    #修改手机号
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name="update_mobile"),
    #我的课程
    # url(r'^mycourse/$', login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"),login_url="/login/"), {"current_page":"mycourse"}, name="mycourse"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    #我的收藏
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),
    #消息
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
    #订单
    url(r'^myorder/$', MyOrderView.as_view(), name="myorder"),
]
