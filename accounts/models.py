from django.db import models
# use djangos inbuilt auth modelto create users
from django.contrib import auth

# Create your models here.
# inherit the model from the auth model which provides you with all the
# requried fields for user creation, return a string representation in the
# form of username with @symbol attched to it.
class User(auth.models.User,auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)
