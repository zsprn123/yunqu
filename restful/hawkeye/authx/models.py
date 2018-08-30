# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./authx/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2397 bytes
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from common.models import CoreModel

class UserManager(BaseUserManager):

    def create_user(self, username, password):
        if username is None:
            raise ValueError('')
        if password is None:
            raise ValueError('')
        user = self.model(username=username)
        user.is_staff = False
        user.set_password(password)
        self.save = user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AbstractUser(AbstractBaseUser, PermissionsMixin, CoreModel):
    """
    
    """
    username = models.CharField(max_length=11, verbose_name='', unique=True)
    fullname = models.CharField(max_length=80, blank=True, verbose_name='')
    thumbnail = models.ImageField(upload_to='thumbnail', verbose_name='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.fullname

    def get_full_name(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return self.is_superuser or perm in self.get_all_permissions()

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        else:
            return True

    class Meta:
        abstract = True


class User(AbstractUser):
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    owner = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user'
        verbose_name = ''
        verbose_name_plural = verbose_name
        permissions = (('view_user', 'Can drive'), )

    def __str__(self):
        return self.username
# okay decompiling ./restful/hawkeye/authx/models.pyc
