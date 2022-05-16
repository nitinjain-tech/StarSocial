from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username





# from django.db import models
# from django.contrib import auth
# import uuid
#
# # Create your models here.
#
# # class MyUUIDModel(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#
# class User(auth.models.User,auth.models.PermissionsMixin):
#
#     def __str__(self):
#         return "@{}".format(self.username)
#
# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     auth_token = models.CharField(max_length=100)
#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.username
