from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q

from apps.organizations.models import CourseOrg, City, Teacher
from apps.operations.models import UserFavorite


# Create your views here.

#讲师详情
class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False#默认收藏状态为未收藏
        #如果已经登陆
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.id):
                teacher_fav = True

        return render(request,"teacher-detail.html",{
            "teacher":teacher,
            "teacher_fav":teacher_fav,
        })


#讲师列表
class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=5, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers":teachers,
            "teacher_nums":teacher_nums,
        })


#机构首页
class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()

        return render(request, "org-detail-homepage.html", {
            "all_courses":all_courses,
            "all_teacher":all_teacher,
            "course_org":course_org,
            "current_page": current_page,
        })

