from django.contrib.auth.hashers import make_password
from django.db import models


class UserModel(models.Model):
    name = models.CharField(max_length=11, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='用户密码', null=True)
    token = models.CharField(max_length=128, null=True, blank=True, verbose_name='token')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        # 为这个类定义一个说明
        verbose_name = "用户表"
        db_table = "user"
        ordering = ['createTime']

    def set_password(self, password):
        self.password = make_password(password)
        return self.password

    def check_password(self, password):
        return (password, self.password)


class FileModel(models.Model):
    name = models.CharField(max_length=50)
    # image = models.ImageField(upload_to="image")
    file = models.FileField(upload_to='static/%Y/%m/%d/')

    class Meta:
        # 为这个类定义一个说明
        verbose_name = "File"
        db_table = "file"
