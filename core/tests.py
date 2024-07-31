from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import Profile

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_creation(self):
        """
        test that profile instance is created when user is created 
        """
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user, self.user)

    def test_profile_fields(self):
        """
        test that the profile fields are correctly set 
        """
        self.profile.full_name = 'Test User'
        self.profile.date_of_birth = date(1990, 1, 1)
        self.profile.phone = '1234567890'
        self.profile.country = 'Test Country'
        self.profile.city = 'Test City'
        self.profile.save()

        self.assertEqual(self.profile.full_name, 'Test User')
        self.assertEqual(self.profile.date_of_birth, date(1990, 1, 1))
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.country, 'Test Country')
        self.assertEqual(self.profile.city, 'Test City')
