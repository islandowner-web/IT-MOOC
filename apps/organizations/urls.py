from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgHomeView
from apps.organizations.views import TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
]
