from django.test import TestCase
from profiles.models import Profile


class TestProfileModel(TestCase):
    def setUp(self):
        self.profile = Profile(firstname="Royhan", lastname="mardista", phone="081342871471", gender="male", "nationality"="ID", photo=)
        self.profile.save()

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)

    def test_profile_representation(self):
        self.assertEqual(self.profile.name, str(self.profile))