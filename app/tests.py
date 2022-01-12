from django.test import TestCase
from .models import Profile, Image
from django.contrib.auth.models import User

# Create your tests here.

class TestProfile(TestCase):
    '''
    Tests the profile class
    '''

    def setUp(self):
        self.user = User.objects.create(username = 'babu')
        self.user.save()
        self.user_profile = Profile(user = self.user, username = 'kenbabu', bio='I came I saw I conquered', profile_pic = 'profile_image')

    def test_instance(self):
        self.assertTrue(isinstance(self.user_profile, Profile))

    def test_save_profile(self):
        self.user_profile.save_profile()
        profiles = Profile.objects.all()

        self.assertTrue(len(profiles) > 0)

    def test_delete_profile(self):
        self.user_profile.save_profile()
        self.user_profile.delete_profile()
        profiles = Profile.objects.all()

        self.assertTrue(len(profiles) == 0)

    def test_search_profile(self):
        self.user_profile.save_profile()
        search_query = 'smith'
        found_profiles = Profile.search_profile(search_query)

        self.assertEqual(found_profiles[0].username, self.user_profile.username)



class TestImage(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='kenny')
        self.user.save()

        self.image = Image(user = self.user, image_path = 'path', image_caption='wonders')

    def test_instance(self):
        self.assertTrue(isinstance(self.image, Image))

    def test_save_image(self):
        self.image.save_image()
        images = Image.objects.all()

        self.assertTrue(len(images)> 0)

    def test_delete_image(self):
        self.image.save_image()
        self.image.delete_image()
        images = Image.objects.all()

        self.assertTrue(len(images) == 0)



