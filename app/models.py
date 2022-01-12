from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model





# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    followers = ManyToManyField(User, related_name='followers', blank=True)
    profile_photo = CloudinaryField('image', null=True )

    def save_profile(self):
        '''
        save profile
        '''
        self.save()

    def delete_profile(self):
        '''
        delete profile
        '''
        self.delete()

    def update_profile(self, new):
        '''
        method that will update the profile
        '''
        self.username = new.username
        self.bio = new.bio
        self.profile_photo = new.profile_photo
        self.save()

    def total_followers(self):
        '''
        method that will return the total no of followers
        '''
        return self.followers.count()



    @classmethod
    def search_profile(cls, search_query):
        profile = cls.objects.filter(username__icontains = search_query)
        return profile

    def __str__(self):
        return self.username 


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_content = models.ImageField(upload_to='profilepic/')
    image_name = models.CharField(max_length=40)
    image_caption = models.TextField(null=True, blank=True)
    total_likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(null=True, auto_now_add=True)


    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_image_caption(self, new_caption):
        self.image_caption = new_caption

    def like_image(self, user):
        self.likes.add(user)

    def total_like(self):
        return self.likes.count()

    def get_comments(self):
        comments = Comment.objects.filter(image = self)
        return comments

    def get_total_likes(self):
        return self.likes.count()


    @classmethod
    def search_image(cls, search_query):
        image = cls.objects.filter(image_name__icontains = search_query)
        return image


    @classmethod
    def get_images(cls, users):
        posts = []
        for user in users:
            images = Image.objects.filter(user = users)
            for image in images:
                posts.append(image)
        return posts
    

    def __str__(self):
        return self.image_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date_created = models.DateTimeField(null=True, auto_now_add=True)


    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    def __str__(self):
        return self.comment_content

class Likes(models.Model):

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


