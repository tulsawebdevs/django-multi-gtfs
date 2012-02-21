from django.db import models

class Feed(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add = True)