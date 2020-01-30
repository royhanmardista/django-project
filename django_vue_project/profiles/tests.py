# Create your tests here.
# class LowonganListAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.username = "john"
#         self.email = "john@snow.com"
#         self.password = "you_know_nothing"

#         self.firstname = "lorem_ipsum"
#         self.lasname = "lorem ipsum dolor sit amet"
#         self.gender = "male"
#         self.nationality = "ID"
#         self.date_of_birth = "1920-04-07"
#         self.phone = "08823443216"
#         # Create image
#         image = Image.new('RGB', (100, 100))
#         tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
#         image.save(tmp_file)

#         self.photo = tmp_file.name

#         self.user = User.objects.create_user(
#             self.username, self.email, self.password
#         )

#         self.profile = Profile.objects.create(
#             user=self.user,
#             firstnama=self.firstname,
#             lastname=self.lastname,
#             gender=self.gender,
#             nationaliry=self.nationality,
#             date_of_birth=self.date_of_birth,
#             phone=self.phone,
#             photo=self.photo

#         )

#         self.company = Perusahaan()
#         self.company.name = self.company_name,
#         self.company.description = self.company_description,
#         self.company.address = self.company_address,
#         self.company.contact_person = self.company_contact,
#         self.company.save()

#         self.user_perusahaan = self.company

#         self.job = Job.objects.create(
#             perusahaan=self.company,
#             position=self.job_title,
#             description=self.job_description,
#         )

#         self.url = reverse("lowongan:list")
#         self.company_url = reverse(
#             "lowongan:detail", kwargs={
#                 "pk": self.company.pk})

import json
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from todos.models import Todo
from todos.serializers import TodoSerializer


class TodoListCreateAPIViewTestCase(APITestCase):
    url = reverse("todos:list")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()


        self.firstname = "lorem_ipsum"
        self.lasname = "lorem ipsum dolor sit amet"
        self.gender = "male"
        self.nationality = "ID"
        self.date_of_birth = "1920-04-07"
        self.phone = "08823443216"
        # Create image
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        self.photo = tmp_file.name

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_todo(self):
        response = self.client.post(self.url, {"name": "Clean the room!"})
        self.assertEqual(201, response.status_code)

    def test_user_todos(self):
        """
        Test to verify user todos list
        """
        Todo.objects.create(user=self.user, name="Clean the car!")
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) == Todo.objects.count())


class TodoDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.todo = Todo.objects.create(user=self.user, name="Call Mom!")
        self.url = reverse("todos:detail", kwargs={"pk": self.todo.pk})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_todo_object_bundle(self):
        """
        Test to verify todo object bundle
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        todo_serializer_data = TodoSerializer(instance=self.todo).data
        response_data = json.loads(response.content)
        self.assertEqual(todo_serializer_data, response_data)

    def test_todo_object_update_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        # HTTP PUT
        response = self.client.put(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

        # HTTP PATCH
        response = self.client.patch(self.url, {"name", "Hacked by new user"})
        self.assertEqual(403, response.status_code)

    def test_todo_object_update(self):
        response = self.client.put(self.url, {"name": "Call Dad!"})
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get("name"), todo.name)

    def test_todo_object_partial_update(self):
        response = self.client.patch(self.url, {"done": True})
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(response_data.get("done"), todo.done)

    def test_todo_object_delete_authorization(self):
        """
            Test to verify that put call with different user token
        """
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_todo_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
