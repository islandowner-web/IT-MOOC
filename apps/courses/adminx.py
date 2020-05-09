import xadmin
from xadmin.layout import Fieldset, Main, Side, Row

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, Order, CourseHomework, CourseHomeworkDetail
from apps.organizations.models import Teacher, CourseOrg

#xadmin界面配置---页头页脚
class GlobalSettings(object):
    site_title = "Cloud·MOOC后台管理系统"
    site_footer = "Cloud·MOOC后台管理系统"

#xadmin界面配置---主题
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class LessonInline(object):
    model = Lesson
    extra = 0
    exclude = ["add_time"] #屏蔽字段不显示


class CourseResourceInline(object):
    model = CourseResource
    style = "tab"
    extra = 1


class NewCourseAdmin(object):
    list_display = ["name", "show_image", "go_to", "degree", "learn_times", "students"]
    search_fields = ["name", "desc", "detail", "degree", "students"]
    list_filter = ["name", "desc", "teacher__name", "detail", "degree", "learn_times", "students"]
    list_editable = ["degree", "desc", "name"]
    ordering = ["-click_nums"]
    inlines = [LessonInline, CourseResourceInline]
    #富文本编辑器
    style_fields = {
        "detail":"ueditor",
    }

    #重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher = self.request.user.teacher)
        return qs

    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset("讲师信息",
                         'teacher','course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset("基本信息",
                         'name', 'desc',
                         Row('learn_times','degree'),
                         Row('category'),
                         'notice', 'detail','image'
                         ),
            ),
            Side(
                Fieldset("访问信息",
                         'fav_nums', 'click_nums', 'students', 'add_time'
                         ),
            ),
        )
        return super(NewCourseAdmin, self).get_form_layout()





class LessonAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    #course__name  course为外键，根据这个外键的name属性进行过滤
    list_filter = ["course__name", "name", "add_time"]

    # 重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    def get_context(self):
        context = super(LessonAdmin, self).get_context()
        # print(context)
        if not self.request.user.is_superuser:
            if 'form' in context:
                context['form'].fields['teacher'].queryset = Teacher.objects.filter(name=self.request.user.teacher)
                context['form'].fields['course'].queryset = Course.objects.filter(teacher=self.request.user.teacher)
                return context
        return context


class VideoAdmin(object):
    list_display = ["course", "lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]
    list_filter = ["course", "lesson", "name", "add_time"]

    # 重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    def get_context(self):
        context = super(VideoAdmin, self).get_context()
        if not self.request.user.is_superuser:
            if 'form' in context:
                context['form'].fields['teacher'].queryset = Teacher.objects.filter(name=self.request.user.teacher)
                context['form'].fields['course'].queryset = Course.objects.filter(teacher=self.request.user.teacher)
                context['form'].fields['lesson'].queryset = Lesson.objects.filter(teacher=self.request.user.teacher)
                return context
        return context


class CourseResourceAdmin(object):
    list_display = ["course", "name", "file", "add_time"]
    search_fields = ["course", "name", "file"]
    list_filter = ["course", "name", "file", "add_time"]

    # 重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
            print(self.request.user.teacher)
        return qs

    # context内form内含有所有可修改的表单，对表单内容进行筛选使教师只能修改自己对应的课程
    def get_context(self):
        context = super(CourseResourceAdmin, self).get_context()
        if not self.request.user.is_superuser:
            if 'form' in context:
                context['form'].fields['teacher'].queryset = Teacher.objects.filter(name=self.request.user.teacher)
                context['form'].fields['course'].queryset = Course.objects.filter(teacher=self.request.user.teacher)
                return context
        return context

class CourseTagAdmin(object):
    list_display = ["course", "tag", "add_time"]
    search_fields = ["course", "tag"]
    list_filter = ["course", "tag", "add_time"]

class OrderAdmin(object):
    list_display = ["order_number", "order_status", "course", "userid", "add_time"]
    search_fields = ["order_number", "order_status", "course", "userid", "add_time"]
    list_filter = ["order_number", "order_status", "course", "userid", "add_time"]


class CourseHomeworkAdmin(object):
    list_display = ["course", "name"]
    search_fields = ["course", "name"]
    list_filter = ["course", "name"]

    # 重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    # context内form内含有所有可修改的表单，对表单内容进行筛选使教师只能修改自己对应的课程
    def get_context(self):
        context = super(CourseHomeworkAdmin, self).get_context()
        # print(context)
        if not self.request.user.is_superuser:
            if 'form' in context:
                context['form'].fields['teacher'].queryset = Teacher.objects.filter(name=self.request.user.teacher)
                context['form'].fields['course'].queryset = Course.objects.filter(teacher=self.request.user.teacher)
                return context
        return context



class CourseHomeworkDetailAdmin(object):
    list_display = ["course", "name", "question", "answer", "jiexi"]
    search_fields = ["course", "name", "question", "answer", "jiexi"]
    list_filter = ["course", "name", "question", "answer", "jiexi"]

    # 重载queryset方法，如果是管理员则返回所有信息，如果是教师只返回教师自己对应的课程等信息
    def queryset(self):
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    #context内form内含有所有可修改的表单，对表单内容进行筛选使教师只能修改自己对应的课程作业
    def get_context(self):
        context = super(CourseHomeworkDetailAdmin, self).get_context()
        # print(context)
        if not self.request.user.is_superuser:
            if 'form' in context:
                # print(context['form'].fields['teacher'].queryset)
                # print(self.request.user.teacher)
                context['form'].fields['teacher'].queryset = Teacher.objects.filter(name=self.request.user.teacher)
                context['form'].fields['course'].queryset = Course.objects.filter(teacher=self.request.user.teacher)
                context['form'].fields['name'].queryset = CourseHomework.objects.filter(teacher=self.request.user.teacher)
            return context
        return context


xadmin.site.register(Course,NewCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(CourseTag,CourseTagAdmin)
xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(CourseHomework,CourseHomeworkAdmin)
xadmin.site.register(CourseHomeworkDetail,CourseHomeworkDetailAdmin)
#xadmin界面配置
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSettings)