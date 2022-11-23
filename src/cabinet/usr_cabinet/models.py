from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email

from cabinet.settings import ALLOWED_USER_TYPES
from .mixins import NameMixin, UserIdMixin


class Manager_(BaseUserManager):
    def _create_student(self, user) -> None:
        student = Student(user=user)
        return student

    def _create_teacher(self, user) -> None:
        teacher = Teacher(user=user)
        # for course in courses: teacher.courses.add(course) -> to add courses if any
        return teacher

    def create_user(
        self, email: str, type: int, password: str = None, **other_fields
    ) -> object:
        """Creates, saves to db and returns created user"""

        if not email:
            raise ValueError("Email should have been provided")
        else:
            validate_email(email)

        if type not in ALLOWED_USER_TYPES.keys():
            raise ValueError(f'Type "{type}" is not a valid user type')

        if not password:
            raise ValueError("Password should have been provided")

        type = UserType(
            enum=type,
        )
        type.save(using=self._db)

        user = self.model(
            email=self.normalize_email(email=email),
            type=type,
            **other_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        print(f"Saved user with type {user.type.enum} {user.type.__class__.__name__}")

        # Filling student and teacher info tables according to user's type

        if user.type.enum == 2:
            # Add institute id if any
            student = self._create_student(user=user)
            student.save(using=self._db)

        if user.type.enum == 3:
            # Add courses if any
            teacher = self._create_teacher(user=user)
            teacher.save(using=self._db)

        return user

    def create_superuser(
        self, email: str, type: str, password: str = None, **other_fields
    ) -> object:
        user = self.create_user(
            email=email,
            type=type,
            password=password,
            **other_fields,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    type = models.ForeignKey(
        "UserType", null=True, on_delete=models.SET_NULL, related_name="users"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = Manager_()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["type"]

    # TODO Maybe someone else could be a staff member?
    @property
    def is_staff(self) -> bool:
        return self.is_admin

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.email

    # TODO Review permissions
    def has_perm(self, perm: str, obj=None) -> bool:
        return True if self.is_admin else False

    def has_module_perms(self, app_label: str) -> bool:
        return True if self.is_admin else False


class Course(NameMixin):
    institutes = models.ManyToManyField(
        "Institute",
        default=None,
    )


class Institute(NameMixin):
    scientific_field = models.CharField(max_length=50)


class UserType(models.Model):
    class Type(models.IntegerChoices):
        STAFF = 1
        STUDENT = 2
        TEACHER = 3

    enum = models.IntegerField(
        choices=Type.choices, 
        unique=True, 
        primary_key=True,
    )


class Student(UserIdMixin):
    institute = models.ForeignKey(
        "Institute",
        related_name="students",
        null=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    objects = Manager_()


class Teacher(UserIdMixin):
    courses = models.ManyToManyField("Course", default=None)

    objects = Manager_()
