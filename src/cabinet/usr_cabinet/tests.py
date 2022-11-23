from django.test import TestCase

from .models import (
    User,
    UserType,
    Student,
    Teacher,
    Institute,
    Course,
)
from cabinet.settings import ALLOWED_USER_TYPES


def get_user(type: str) -> dict:
    return {
        "email": f"{type}@test.com",
        "type": type,
        "first_name": "Test",
        "last_name": ALLOWED_USER_TYPES[type].capitalize(),
        "password": "123",
    }


STAFF = get_user(1)
STUDENT = get_user(2)
TEACHER = get_user(3)


class UserCreationTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(**STAFF)
        User.objects.create_user(**STUDENT)
        User.objects.create_user(**TEACHER)

    def test_user_creation(self):
        staff = User.objects.get(email=STAFF["email"])
        student = User.objects.get(email=STUDENT["email"])
        teacher = User.objects.get(email=TEACHER["email"])

        self.assertEqual(staff, User.objects.get(email=STAFF["email"]))
        self.assertEqual(student, User.objects.get(email=STUDENT["email"]))
        self.assertEqual(teacher, User.objects.get(email=TEACHER["email"]))

    def test_invalid_fields(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()

        # No password
        with self.assertRaises(ValueError):
            User.objects.create_user(email="test@t.com", type=1)

        with self.assertRaises(ValueError):
            User.objects.create_user(email="test2@t.com", type="invalid")


class UserRelationsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(**STAFF)
        User.objects.create_user(**STUDENT)
        User.objects.create_user(**TEACHER)

    def test_user_type_table(self):
        staff = User.objects.get(email=STAFF["email"])
        student = User.objects.get(email=STUDENT["email"])
        teacher = User.objects.get(email=TEACHER["email"])

        staff_type = UserType.objects.get(enum=1)
        self.assertEqual(staff_type, staff.type)

        student_type = UserType.objects.get(enum=2)
        self.assertEqual(student_type, student.type)

        teacher_type = UserType.objects.get(enum=3)
        self.assertEqual(teacher_type, teacher.type)

        # User type cascade drop
        staff_type.delete()
        staff = User.objects.get(email=STAFF["email"])
        self.assertEqual(staff.type, None)
        student_type.delete()
        student = User.objects.get(email=STUDENT["email"])
        self.assertEqual(student.type, None)
        teacher_type.delete()
        teacher = User.objects.get(email=TEACHER["email"])
        self.assertEqual(teacher.type, None)

    def test_student_table(self):
        student_user: User = User.objects.get(email=STUDENT["email"])
        Student.objects.get(user_id=student_user.id)

        # Query non-existing id
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(user_id=10000)

        # Cascade delete student after user drop
        deleted_user_id = student_user.id
        student_user.delete()

        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(user_id=deleted_user_id)

    def test_teacher_table(self):
        teacher_user: User = User.objects.get(email=TEACHER["email"])
        Teacher.objects.get(user_id=teacher_user.id)

        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(user_id=10000)

        # Cascade delete teacher after user drop
        deleted_user_id = teacher_user.id
        teacher_user.delete()

        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(user_id=deleted_user_id)

    def test_institute_table(self):
        user = User.objects.get(email=STUDENT["email"])
        student = Student.objects.get(user_id=user.id)
        economics_institute = Institute.objects.create(
            scientific_field="Economy",
            name='Insistute of Economy',
        )
        economics_institute.students.add(student)
        self.assertEqual(
            user.id,
            economics_institute.students.get(user_id=user.id).user_id,
        )

        # TODO test institute drop

    def test_course_table(self):
        user = User.objects.get(email=TEACHER["email"])
        teacher = Teacher.objects.get(user_id=user.id)
        institute = Institute.objects.create(
            scientific_field="Economy",
            name='Insistute of Economy',
        )
        course = Course.objects.create(name='Microeconomics')
        course.institutes.add(institute)
        teacher.courses.add(course)
        self.assertEqual(
            user.id,
            course.teacher_set.get(user_id=user.id).user_id
        )

        # TODO test course drop
