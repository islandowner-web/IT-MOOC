from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
from DjangoUeditor.models import UEditorField
# Create your models here.


#订单表
class Order(models.Model):
    order_number = models.CharField(max_length=64, verbose_name="订单号")
    status_choices = ((0, '未支付'), (1, '已支付'))
    order_status = models.IntegerField(choices=status_choices, default=0, verbose_name="支付状态")
    course = models.ForeignKey(to='Course', on_delete=models.CASCADE, verbose_name="课程名")
    userid = models.CharField(max_length=60, verbose_name="用户编号")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "课程订单"


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="课程机构")
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述",max_length=300)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField(verbose_name="难度", choices=(("cj","初级"), ("zj","中级"), ("gj","高级")), max_length=2)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")
    category = models.CharField(default="后端开发", max_length=20, verbose_name="课程类别")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="courses/ueditor/files/", default="")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    needpay = models.BooleanField(default=False, verbose_name="是否付费课程")
    price = models.IntegerField(default=0, verbose_name="价格")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()#统计课程章节数

    #管理系统内显示图片而非src路径
    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}' height=125px width=222px>".format(self.image.url))
    show_image.short_description = "图片"

    #链接直接跳到课程本身
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))
    go_to.short_description = "跳转"



class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag



class Lesson(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class CourseResource(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    file = models.FileField(upload_to="course/resource//%Y/%M", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseHomework(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程", default='')
    name = models.CharField(max_length=100, verbose_name="名称", default='')

    class Meta:
        verbose_name = "课程作业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseHomeworkDetail(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name = models.ForeignKey(CourseHomework, on_delete=models.CASCADE, null=False, default='', verbose_name="所属作业")
    question = models.CharField(max_length=100, verbose_name="题目")
    cone = models.CharField(max_length=100, verbose_name="选项A")
    ctwo = models.CharField(max_length=100, verbose_name="选项B")
    cthree = models.CharField(max_length=100, verbose_name="选项C")
    cfour = models.CharField(max_length=100, verbose_name="选项D")
    answer =  models.CharField(verbose_name="答案", choices=(("A","A"), ("B","B"), ("C","C"), ("D","D")), max_length=2)
    jiexi = models.CharField(max_length=100, verbose_name="解析")

    class Meta:
        verbose_name = "课程作业题目"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return "课程作业题目"