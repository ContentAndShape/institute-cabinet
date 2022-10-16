from django.db import models
from django.contrib.auth.models import User


class UserReprMixin(User):

    class Meta:
        ordering = ['last_name']

    def __str__(self) -> str:
        return self.get_full_name()


class NameMixin(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Course(NameMixin):
    related_institute = models.ForeignKey('Institute', null=True, on_delete=models.SET_NULL)


class Institute(NameMixin):
    scientific_field = models.CharField(max_length=50)


class Student(UserReprMixin):
    institute = models.ForeignKey('Institute', null=True, on_delete=models.SET_NULL)


class Teacher(UserReprMixin):
    courses = models.ManyToManyField('Course')

