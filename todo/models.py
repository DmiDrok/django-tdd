from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.CharField(max_length=255, blank=False, null=True)
    list = models.ForeignKey(to='List', on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['id']
        unique_together = ['text', 'list']

    def __str__(self):
        return self.text

class List(models.Model):
    
    def get_absolute_url(self):
        return reverse('lists', kwargs={'list_id': self.pk})
