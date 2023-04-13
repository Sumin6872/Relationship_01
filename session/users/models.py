from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, password, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

    def create_normaluser(self, username, password, **kwargs):
        self.create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        self.create_user(username, password, **kwargs)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username' 

    username = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()  

    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname
