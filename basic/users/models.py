from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your models here.
class Profile(models.Model):
    ROLES = (
                ('SUPER_ADMIN','Super Admin'),
                ('EVENT_MANAGER','Event Manager'),
                ('LIVE_TELECASTER','Live Telecaster'),
            );

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLES)
    address = models.TextField()
    city = models.CharField(max_length=255,null = True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     if self.user is not None:
    #         return self.user.username


class CustomUser():

    def authenticate_user(self,*args,**kwargs):
        """
        User Authentication
        """
        try:
            user = authenticate(username=kwargs.get('email',None), password=kwargs.get('password',None))
            if user is not None:
                # if not user.is_active:
                #     return {"status": False, "data": "User is inactive Status"}
                token, created  = Token.objects.get_or_create(user=user)
                return {"status" : True , "token" : token.key}
            else:
                return {"status" : False, "data" : "Invalid Email Address or password"}
        except Exception as e:
            return {"status": False, "data" : str(e)}
