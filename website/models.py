from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    pub_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Artwork(models.Model):
    reg_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    def __str__(self):
        return str(self.reg_date)
#
