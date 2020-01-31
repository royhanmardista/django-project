from django.core.files.uploadedfile import SimpleUploadedFile
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Profile
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("register")

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "test123123",
            "confirm_password": "test123123"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("message" in json.loads(response.content))
        self.assertTrue("user" in json.loads(response.content))

    def test_invalid_password(self):
        """
        Test to verify that a post call with password not matched
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "INVALID_PASSWORD"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"error": "password not matched"}
        )
        self.assertEqual(400, response.status_code)

    def test_invalid_password_2(self):
        """
        Test to verify that a post call with password to sort
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "1234",
            "confirm_password": "1234"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': {'password': [
                'Ensure this field has at least 8 characters.']}}
        )
        self.assertEqual(400, response.status_code)

    def test_invalid_username(self):
        """
        Test to verify that a post call invalid username character length
        """
        user_data = {
            "username": "t",
            "email": "test@testuser.com",
            "password": "test1234",
            "confirm_password": "test1234"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': {'username': [
                'Ensure this field has at least 3 characters.']}}
        )
        self.assertEqual(400, response.status_code)

    def test_invalid_email(self):
        """
        Test to verify that a post call invalid email format
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser",
            "password": "test1234",
            "confirm_password": "test1234"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': {'email': ['Enter a valid email address.']}}
        )
        self.assertEqual(400, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "test123123",
            "confirm_password": "test123123"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'username already exist'}
        )
        self.assertEqual(400, response.status_code)

    def test_unique_email_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "test123123",
            "confirm_password": "test123123"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "username": "testuser2",
            "email": "test@testuser.com",
            "password": "123123",
            "confirm_password": "123123"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'email already exist'}
        )
        self.assertEqual(400, response.status_code)

    def test_blank_data(self):
        """
        Test to verify that a post call with blank data
        """
        user_data = {
            "username": "",
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "password"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': {'username': ['This field may not be blank.']}}
        )
        self.assertEqual(400, response.status_code)

    def test_empty_data(self):
        """
        Test to verify that a post call with empty data
        """
        user_data = {
            "email": "test@testuser.com",
            "password": "password",
            "confirm_password": "password"
        }
        response = self.client.post(self.url, user_data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': {'username': ['This field is required.']}}
        )
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("login")

    def setUp(self):
        self.username = "test"
        self.email = "test@gmail.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def test_authentication_username_not_found(self):
        """
        Login fail user not found
        """
        response = self.client.post(
            self.url, {"username": "snowman", "password": "password"})
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Username not found'}
        )
        self.assertEqual(404, response.status_code)

    def test_authentication_without_password(self):
        """
        Login fail user no  password provided
        """
        response = self.client.post(self.url, {"username": "snowman"})
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'You need to provide both password and username'}
        )
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        """
        Login fail wrong password
        """
        response = self.client.post(
            self.url, {"username": self.username, "password": "I_know"})
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Wrong password'}
        )
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        """
        Login success
        """
        response = self.client.post(
            self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))
        self.assertTrue("message" in json.loads(response.content))


class GetAllUsers(APITestCase):
    url = reverse("allusers")

    def get_all_user(self):
        """
        Getting all users success
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue("users" in json.loads(response.content))
        self.assertTrue(len(json.loads(response.content))
                        == User.objects.count())


class GetLoggedUser(APITestCase):
    url = reverse("login")
    url2 = reverse("loggeduser")

    def setUp(self):
        self.username = "test"
        self.email = "test@gmail.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

    def test_get_the_logged_user(self):
        """
        getting the logged user success
        """
        response = self.client.post(
            self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))
        self.assertTrue("message" in json.loads(response.content))

        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        access_token = 'jwt ' + token
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        response = self.client.get(self.url2)
        self.assertEqual(200, response.status_code)
        self.assertTrue("user" in json.loads(response.content))

    def test_get_the_logged_user_fail_not_login(self):
        """
        getting the logged user fail not login
        """
        response = self.client.post(
            self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))
        self.assertTrue("message" in json.loads(response.content))

        response = self.client.get(self.url2)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'detail': 'Authentication credentials were not provided.'}
        )
        self.assertEqual(401, response.status_code)

from django.core.files.uploadedfile import SimpleUploadedFile

class ProfileCreateAPIViewTestCase(APITestCase):
    url = reverse('createprofile')
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        access_token = 'jwt ' + token
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        self.image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

    def test_create_profile_success(self):
        """
        Test to verify user creating profile success
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("profile" in json.loads(response.content))
        self.assertTrue("user" in json.loads(response.content))
        self.assertTrue("message" in json.loads(response.content))

    def test_create_profile_fail_empty_firstname(self):        
        """
        Test to verify user creating profile fail, no firstname
        """
        profile_data = {
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'firstname': ['This field is required.']}
        )

    def test_create_profile_fail_blank_firstname(self):        
        """
        Test to verify user creating profile fail, blank firstname
        """
        profile_data = {
            "firstname": "",
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'firstname': ['This field may not be blank.']}
        )

    def test_create_profile_fail_invalid_firstname(self):        
        """
        Test to verify user creating profile fail, firstname contain number
        """
        profile_data = {
            "firstname": "21111",
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'firstname': ['Can Only enter alphabet']}
        )

    def test_create_profile_fail_invalid_firstname(self):        
        """
        Test to verify user creating profile fail, firstname minimal 3 character
        """
        profile_data = {
            "firstname": "a",
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'firstname': ['Min Length is 3 Characters']}
        )

    def test_create_profile_fail_gender_empty(self):        
        """
        Test to verify user creating profile fail, gender empty
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'gender': ['This field is required.']}
        )
    
    def test_create_profile_fail_invalid_gender_choice(self):        
        """
        Test to verify user creating profile fail, invalid gender chice
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "whatever",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'gender': ['"whatever" is not a valid choice.']}
        )

    def test_create_profile_fail_invalid_date_format(self):        
        """
        Test to verify user creating profile fail, invalid date format
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "190-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("date_of_birth" in json.loads(response.content))

    def test_create_profile_fail_date_in_the_future(self):        
        """
        Test to verify user creating profile fail, birthdate in the future
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "2920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'date_of_birth': ['Birth Date cannot be in the future!']}
        )

    def test_create_profile_fail_older_then_100_years(self):        
        """
        Test to verify user creating profile fail, older then 100 years
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1020-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'date_of_birth': ['Age cannot be older then 100 years']}
        )

    def test_create_profile_fail_empty_date_of_birth(self):        
        """
        Test to verify user creating profile fail, ompty birthdate
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'date_of_birth': ['This field is required.']}
        )

    def test_create_profile_fail_empty_nationality(self):        
        """
        Test to verify user creating profile fail, empty nationality
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'nationality': ['This field is required.']}
        )
    def test_create_profile_fail_invalid_nationality(self):        
        """
        Test to verify user creating profile fail, invalid nationality
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "nationality" : 'KOR',
            "phone": "081342871471",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'nationality': ['"KOR" is not a valid choice.']}
        )

    def test_create_profile_fail_invalid_phonenumber(self):        
        """
        Test to verify user creating profile fail, invalid phonenumber
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "nationality" : 'JP',
            "phone": "1222",
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'phone': ['The phone number entered is not valid.']}
        )
    
    def test_create_profile_fail_empty_phonenumber(self):        
        """
        Test to verify user creating profile fail, empty phonenumber
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "nationality" : 'JP',
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'phone': ['This field is required.']}
        )

    def test_create_profile_fail_already_have_profile(self):        
        """
        Test to verify user creating profile fail, already have profile
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "phone": "081342871471",
            "nationality" : 'JP',
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(201, response.status_code)        
        
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'You already created a profile'}
        )
    
    def test_create_profile_fail_nonunique_phonenumber(self):        
        """
        Test to verify user creating profile fail, nonunique phonenumber
        """
        profile_data = {
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender" : "male",
            "date_of_birth": "1990-04-07",
            "phone": "081342871471",
            "nationality" : 'JP',
            "photo": self.image
        }
        response = self.client.post(self.url, profile_data)
        self.assertEqual(201, response.status_code)        
        

        self.username = "john23"
        self.email = "john23@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        access_token = 'jwt ' + token
        self.client.credentials(HTTP_AUTHORIZATION=access_token)
        
        response = self.client.post(self.url, profile_data)
        self.assertEqual(400, response.status_code)

class ProfileUpdatePIViewTestCase(APITestCase):
    
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        
        self.image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        profile_data = {
            "user" : self.user.id,
            "firstname": "naruto",
            "lastname": "uzumaki",
            "gender": "male",
            "date_of_birth": "1920-04-07",
            "nationality": "JP",
            "phone": "081342871471",
            "photo": self.image
        }        
        self.profile = Profile(profile_data)
        self.url = reverse("read_update_delete", kwargs={"pk": self.profile.pk})

        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        access_token = 'jwt ' + token
        self.client.credentials(HTTP_AUTHORIZATION=access_token)        

    def get_profile_byId_success(self):
        print('dddddddddddddddddddddddddddddd')
        response = self.client.get(self.url, profile_data)
        print(response.content)
        self.assertEqual(11, response.status_code)

