from http import HTTPStatus
from rest_framework.test import APITestCase


class PersonAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/person/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class FacultyAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/faculty/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class DepartmentAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/department/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ProgrammeAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/programme/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class StaffAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class StudentAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/student/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CourseAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/course/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class RegisteredStudentAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/registered_student/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class StudentAttendanceAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/student_attendance/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CourseAttendanceAPITest(APITestCase):

    def test_api_url_exist(self):
        response = self.client.get('/api/course_attendance/')
        self.assertEqual(response.status_code, HTTPStatus.OK)