from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from  apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView
from  apps.users.views import MyCourseView, MyFavCourseView, MyMessageView, MyOrderView, MyFavTeacherView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name="update_mobile"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
    url(r'^myorder/$', MyOrderView.as_view(), name="myorder"),
]
