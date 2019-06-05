from django.db import models
from django.conf import settings
import os


# Create your models here.

def get_constant_image_path(instance, filename):
    return os.path.join('media_resources', 'images', filename)


class StaticImage(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_constant_image_path, null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)


class Character(models.Model):
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=300)
    birth_year = models.CharField(max_length=50)
    expiration_year = models.CharField(max_length=50)
    chosen_user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CharacterUser')
    image = models.ForeignKey(StaticImage, on_delete=models.DO_NOTHING)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.role


class CharacterBio(models.Model):
    bioType = models.CharField(max_length=32)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    bioText = models.CharField(max_length=512)

    def __str__(self):
        return str(self.id) + " : " + self.bioText


class CharacterUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    drinks = models.IntegerField(default=0)
