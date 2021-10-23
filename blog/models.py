from django.db import models


class UserGroup(models.Model):
    name = models.CharField(max_length=32)


class UserInfo(models.Model):
    user_grade = (
        (1, '普通用户'),
        (2, 'VIP用户'),
        (3, '超级VIP用户'),
    )

    user_type = models.IntegerField(choices=user_grade)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey('UserGroup', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role')


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Role(models.Model):
    title = models.CharField(max_length=32)