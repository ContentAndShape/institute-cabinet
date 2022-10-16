from django.db import models
from django.contrib.auth.models import User


class UserRepr(User):

    def __str__(self) -> str:
        return self.get_full_name()


class UserIdMixin(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class NameMixin(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Course(NameMixin):
    related_institute = models.ForeignKey('Institute', on_delete=models.SET_NULL)


class Institute(NameMixin):
    ...


class Student(UserIdMixin, UserRepr):
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE)


class Teacher(UserIdMixin, UserRepr):
    courses = models.ManyToManyField('Course')

