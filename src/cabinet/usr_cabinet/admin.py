from django.contrib import admin
from .models import Course, Institute, Student, Teacher


admin.site.register(Course)
admin.site.register(Institute)
admin.site.register(Student)
admin.site.register(Teacher)