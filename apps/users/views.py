from django.shortcuts import render
from django.views.generic.base import View#通用模版类
from django.contrib.auth import authenticate, login, logout#用户登陆验证
from django.http import HttpResponseRedirect, JsonResponse #登陆后url重定向
from django.urls import reverse #url反转
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, UpdateMobileForm
from apps.users.forms import UploadImageForm, UserInfoForm, ChangePwdForm

from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from Education_106.settings import yp_apikey,REDIS_PORT,REDIS_HOST
from apps.users.models import UserProfile
from apps.operations.models import UserCourse, UserFavorite,UserMessage, Banner
from apps.organizations.models import Teacher
from apps.courses.models import Course, Order

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import redis
from django.contrib.auth.mixins import LoginRequiredMixin#登陆验证
# Create your views here.

#用户验证查询
class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None

#订单
class MyOrderView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myorder"
        orders = Order.objects.filter(userid=request.user.id).order_by("-add_time")

        return render(request, "usercenter-myorder.html", {
            "orders":orders,
            "current_page": current_page
        })



#未读消息
def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums':request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}



#消息
class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=5, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages":messages,
            "current_page":current_page
        })


#我的收藏---course
class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html",{
            "course_list":course_list,
            "current_page":current_page
        })



# 我的收藏---teacher
class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, "usercenter-fav-teacher.html",{
            "teacher_list":teacher_list,
            "current_page":current_page
        })



#我的课程
class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'mycourse'#用于页面左侧导航栏指示选中的状态
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html",{
            "my_courses":my_courses,
            "current_page":current_page
        })


#修改手机号码
class ChangeMobileView(LoginRequiredMixin, View):
    login_url = "/login/"
    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            #已经存在的记录不能重复注册
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile":"该手机号码已经被占用"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(mobile_form.errors)


#修改密码
class ChangePwdView(LoginRequiredMixin, View):

    login_url = "/login/"
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            user = request.user
            user.set_password(pwd1)
            user.save()

            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(pwd_form.errors)


#修改头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        #处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

#个人资料
class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"#用于页面左侧导航栏指示选中的状态
        captcha_form = RegisterGetForm()
        return render(request,"usercenter-info.html",{
            "captcha_form":captcha_form,
            "current_page":current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(user_info_form.errors)

#注册
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form":register_get_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form":register_get_form,
                "register_post_form": register_post_form
            })

#登陆
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        banners = Banner.objects.all()[:3]
        return render(request, "login.html",{
            "login_form":login_form,
            "next":next,
            "banners":banners
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            #没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": d_form,
                                                  "banners":banners,
                                                  "dynamic_login":dynamic_login})

#手机验证码
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            #随机生成数字验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 300)#5分钟过期
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key,value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)

#注销
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

#登陆
class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        banners = Banner.objects.all()[:3]

        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html",{
            "login_form":login_form,
            "next":next,
            "banners":banners,
        })

    def post(self, request, *args, **kwargs):
        #通过forms.py进行表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():

            #----------------------------通过forms.py进行表单验证并拿取数据-------------
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # ----------------------------------------------------------------------
            #authenticate用于通过用户名和密码查询用户是否存在
            user = authenticate(username=user_name, password=password)
            if user is not None:
                #查询到用户⬆，登陆成功⬇
                login(request, user)
                #登陆成功后回首页
                next = request.GET.get("next","")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                #未查询到用户,回注册页
                return render(request, "login.html", {"msg":"用户名或密码错误", "login_form":login_form, "banners":banners})

        else:
            return render(request, "login.html", {"login_form": login_form,
                                                  "banners":banners})