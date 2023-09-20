from django.db import models


class user(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    userType = models.IntegerField()

    # userType = 0 为未授权
    # userType = 1 宿管
    # userType = 2 老师
    # userType = 3 ADMIN

    def __str__(self):
        return f'user {self.id}'


# Dormitory 模型
class Dormitory(models.Model):
    building = models.IntegerField()  # 楼号
    room = models.IntegerField()  # 房间号
    score = models.IntegerField()  # 分数

    def __str__(self):
        return f'Dormitory {self.id}'


# bedInfo 模型
class BedInfo(models.Model):
    bedNumber = models.IntegerField()  # 床位号
    dormitory = models.ForeignKey("Dormitory", on_delete=models.CASCADE)  # 与Dormitory建立外键关联
    bedUsername = models.CharField(max_length=10)  # 床位使用人姓名
    bedUserTel = models.CharField(max_length=13)  # 床位使用人电话
    bedUserNo = models.CharField(max_length=10)  # 床位使用人学号

    def __str__(self):
        return f'BedInfo {self.id}'
