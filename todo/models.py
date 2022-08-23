from django.db import models


class Item(models.Model):
    text = models.CharField(max_length=255, default='', null=True)
    list = models.ForeignKey(to='List', on_delete=models.CASCADE, default=None)


class List(models.Model):
    pass 
