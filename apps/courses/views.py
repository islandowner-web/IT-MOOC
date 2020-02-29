from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin#登陆验证
from django.db.models import Q

from apps.courses.models import Course, CourseTag, CourseResource, Video, Order, CourseHomework, CourseHomeworkDetail
from apps.operations.models import UserFavorite, UserCourse, CourseComments

import uuid
from utils.pay import AliPay


# Create your views here.

#向支付宝提交支付数据
def purchase(request, course_id):
    if request.user.is_authenticated:
        course_obj = Course.objects.get(id=course_id)
        userid = request.user.id


        order_number = str(uuid.uuid4())
        Order.objects.create(
            order_number=order_number,
            course=course_obj,
            userid=userid,
        )

        alipay = AliPay(
            appid="2016101600696348",  # APPID
            app_notify_url='http://106.12.115.136:8000/check_order/',  # 支付宝会向这个地址发送post请求
            return_url='http://127.0.0.1:8000/show_msg/',  # 支付宝会向这个地址发送get请求
            app_private_key_path='keys/app_private_2048.txt',  # 应用私钥
            alipay_public_key_path='keys/alipay_public_2048.txt',  # 支付宝公钥
            debug=True,  # 默认是False
        )

        query_params = alipay.direct_pay(
            subject=course_obj.name,  # 商品描述
            out_trade_no=order_number,  # 订单号
            total_amount=course_obj.price,  # 交易金额(单位是元，保留两位小数)
            # username=request.user.username
        )
        print(query_params)

        pay_url = 'https://openapi.alipaydev.com/gateway.do?{0}'.format(query_params)
        return redirect(pay_url)

    else:
        return HttpResponse('尚未登陆')


#支付宝返回数据并且确认支付状态
def show_msg(request):
    if request.method == 'GET':
        alipay = AliPay(
            appid="2016101600696348",  # APPID
            app_notify_url='http://106.12.115.136:8000/check_order/',
            return_url='http://127.0.0.1:8000/show_msg/',
            app_private_key_path='keys/app_private_2048.txt',  # 应用私钥
            alipay_public_key_path='keys/alipay_public_2048.txt',  # 支付宝公钥
            debug=True,  # 默认是False
        )
        params = request.GET.dict()  # 获取请求携带的参数并转换成字典类型

        print(request.GET)
        print(params)
        print(type(params))
        sign = params.pop('sign', None)  # 获取sign的值
        # 对sign参数进行验证
        status = alipay.verify(params, sign)
        if status:
            # 支付成功修改订单状态为已支付
            out_trade_no = params['out_trade_no']
            print(out_trade_no)
            userid = request.user.id
            print(userid)
            Order.objects.filter(order_number=out_trade_no).update(order_status=1, userid=userid)
            return render(request, 'show_msg.html', {'msg': '支付成功',
                                                     'params': params})

        else:
            return render(request, 'show_msg.html', {'msg': '支付失败'})
    else:
        return render(request, 'show_msg.html', {'msg': '只支持GET请求，不支持其它请求'})






#视频播放
class VideoView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        #获取章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        #查询用户是否学习过该课程，没有则新建记录保存
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        #获取课程资源
        course_resource = CourseResource.objects.filter(course=course)
        # 获取课程作业
        course_homework = CourseHomework.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resource": course_resource,
            "video": video,
            "course_homework": course_homework,
        })


#课程作业
class HomeworkView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, course_id, homework_id, *args, **kwargs):

        # 获取课程详情
        course = Course.objects.get(id=int(course_id))

        print(homework_id)
        print(course_id)
        homeworkss = CourseHomeworkDetail.objects.filter(name=homework_id, course=course_id)
        print(homeworkss)
        return render(request, 'coursehomework.html', {
            "homeworkss": homeworkss,
            "course": course,
        })


#课程评论
class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        # 获取章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        #获取评论
        comments = CourseComments.objects.filter(course=course)

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 查询用户是否学习过该课程，没有则新建记录保存
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        # 获取课程资源
        course_resource = CourseResource.objects.filter(course=course)
        # 获取课程作业
        course_homework = CourseHomework.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resource": course_resource,
            "comments": comments,
            "course_homework": course_homework
        })


#课程章节信息
class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"  #如果未登陆，则跳转到登陆页面

    def get(self, request, course_id, *args, **kwargs):
        #获取章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        #查询用户是否学习过该课程，没有则新建记录保存
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        #获取课程资源
        course_resource = CourseResource.objects.filter(course=course)
        #获取课程作业
        course_homework = CourseHomework.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resource": course_resource,
            "course_homework": course_homework,
        })


#课程详情
class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        #获取课程详情
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 验证课程是否已经购买
        order = Order.objects.filter(userid=request.user.id, course_id=course_id, order_status=1)
        pay_status = 0
        if order:
            pay_status = 1

        #获取收藏状态
        has_fav_course = False #默认课程收藏状态
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True


        # 课程推荐
        tags = course.coursetag_set.all()#找到所有把课程标签
        tag_list = [tag.tag for tag in tags]#课程标签数组
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)#找相似标签去重复
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "related_courses": related_courses,
            "pay_status": pay_status,
        })


#课程列表
class CourseListView(View):
    def get(self, request, *args, **kwargs):
        #获取课程列表信息
        all_courses = Course.objects.order_by("-add_time")

        #获取课程总数
        course_nums = all_courses.count()

        #热门课程推荐
        # hot_courses = Course.objects.order_by("-click_nums")[:3]

        #热门课程推荐重写
        if request.user.is_authenticated:
            my_courses = UserCourse.objects.filter(user=request.user)#找到所有学习的课程
            if my_courses.count() == 0:
                hot_courses = Course.objects.order_by("-click_nums")[:3]
            else:
                tag_list = []
                for c in my_courses:
                    all_tag = c.course.coursetag_set.all()
                    for tag in all_tag:
                        tag_list.append(tag.tag)
                course_tags = CourseTag.objects.filter(tag__in=tag_list)[:4]  #找标签在标签列表里的课程，最多四个
                hot_courses = set()  # set()类型不允许重复
                for course_tag in course_tags:
                    hot_courses.add(course_tag.course)
        else:
            hot_courses = Course.objects.order_by("-click_nums")[:3]



        #搜索关键词
        keywords = request.GET.get("keywords","")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))

        #课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        elif sort == "price":
            all_courses = all_courses.filter(needpay=1)

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=9, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "keywords": keywords,
            "s_type": s_type,
            "course_nums": course_nums,
        })

