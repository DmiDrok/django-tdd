from django.db import models


class Item(models.Model):
    text = models.CharField(max_length=255, default='', null=True)
