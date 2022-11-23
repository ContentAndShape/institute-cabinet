from django.test import TestCase

from .models import User, UserType, Student, Teacher
from cabinet.settings import ALLOWED_USER_TYPES


def get_user(type: str) -> dict:
    return {
        'email': f'{type}@test.com',
        'type': type,
        'first_name': 'Test',
        'last_name': ALLOWED_USER_TYPES[type].capitalize(),
        'password': '123',
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
        staff = User.objects.get(email=STAFF['email'])
        student = User.objects.get(email=STUDENT['email'])
        teacher = User.objects.get(email=TEACHER['email'])

        self.assertEqual(staff, User.objects.get(email=STAFF['email']))
        self.assertEqual(student, User.objects.get(email=STUDENT['email']))
        self.assertEqual(teacher, User.objects.get(email=TEACHER['email']))

    def test_invalid_fields(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()

        # No password
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@t.com', type=1)

        with self.assertRaises(ValueError):
            User.objects.create_user(email='test2@t.com', type='invalid')


class UserRelationsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(**STAFF)
        User.objects.create_user(**STUDENT)
        User.objects.create_user(**TEACHER)

    def test_user_type_table(self):
        staff = User.objects.get(email=STAFF['email'])
        student = User.objects.get(email=STUDENT['email'])
        teacher = User.objects.get(email=TEACHER['email'])

        staff_type = UserType.objects.get(type='staff')
        self.assertEqual(staff_type, staff.type)

        student_type = UserType.objects.get(type='student')
        self.assertEqual(student_type, student.type)

        teacher_type = UserType.objects.get(type='teacher')
        self.assertEqual(teacher_type, teacher.type)

        # User type cascade drop
        staff_type.delete()
        staff = User.objects.get(email=STAFF['email'])
        self.assertEqual(staff.type, None)
        student_type.delete()
        student = User.objects.get(email=STUDENT['email'])
        self.assertEqual(student.type, None)
        teacher_type.delete()
        teacher = User.objects.get(email=TEACHER['email'])
        self.assertEqual(teacher.type, None)

    def test_student_table(self):
        student_user: User = User.objects.get(email=STUDENT['email'])
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
        teacher_user: User = User.objects.get(email=TEACHER['email'])
        Teacher.objects.get(user_id=teacher_user.id)

        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(user_id=10000)

        # Cascade delete teacher after user drop
        deleted_user_id = teacher_user.id
        teacher_user.delete()

        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(user_id=deleted_user_id)

    def test_institute_table(self):
        ...
        # TODO test institute relation to students

    def test_course_table(self):
        ...
        # TODO test course relation to teachers
