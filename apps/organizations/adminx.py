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
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]
    list_editable = ["name", "desc"]

xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(City,CityAdmin)