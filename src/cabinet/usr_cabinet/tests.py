from django.test import TestCase

from .models import User


def get_user(type: str) -> dict:
    return {
        'email': f'{type}@test.com',
        'type': type,
        'first_name': 'Test',
        'last_name': type.capitalize(),
        'password': '123',
    }


ADMIN = get_user('admin')
STUDENT = get_user('student')
TEACHER = get_user('teacher')


class UserTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(**ADMIN)
        User.objects.create_user(**STUDENT)
        User.objects.create_user(**TEACHER)

    def test_user_fields(self):
        admin = User.objects.get(email=ADMIN['email'])
        student = User.objects.get(email=STUDENT['email'])
        teacher = User.objects.get(email=TEACHER['email'])

        for key, val in ADMIN.items():
            self.assertEqual(val, admin.__dict__[key])

        for key, val in STUDENT.items():
            self.assertEqual(val, student.__dict__[key])

        for key, val in TEACHER.items():
            self.assertEqual(val, teacher.__dict__[key])

    def test_user_cascade_delete(self):
        '''
        Test cascade deletion of admin, student, teacher after user instance delteion
        '''
        ...
