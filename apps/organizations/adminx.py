import xadmin

from apps.organizations.models import Teacher, CourseOrg, City

class TeacherAdmin(object):
    list_display = ["org", "name"]
    search_fields = ["org", "name"]
    list_filter = ["org", "name"]

class CourseOrgAdmin(object):
    list_display = ["name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc"]
    style_fields = {
        "desc": "ueditor",
    }

class CityAdmin(object):
    #list_display指明cms列表页要显示的城市表的字段
    list_display = ["id", "name", "desc"]
    #加搜索框，能根据name和desc进行搜索，如上海和魔都都能进行搜索
    search_fields = ["name", "desc"]
    #过滤字段,过滤器
    list_filter = ["name", "desc", "add_time"]
    #可直接编辑字段，在页面列表中直接修改
    list_editable = ["name", "desc"]

xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(City,CityAdmin)