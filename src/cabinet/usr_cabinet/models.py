from django.db import models

from .mixins import NameMixin, UserReprMixin


class Course(NameMixin):
    related_institute = models.ForeignKey(
        'Institute', related_name='courses', null=True, on_delete=models.SET_NULL)


class Institute(NameMixin):
    scientific_field = models.CharField(max_length=50)


class Student(UserReprMixin):
    institute = models.ForeignKey(
        'Institute', related_name='students', null=True, on_delete=models.SET_NULL)


class Teacher(UserReprMixin):
    courses = models.ManyToManyField('Course')

