from django.db import models

# Create your models here.
class File(models.Model):
    created = models.DateTimeField(verbose_name='create', auto_now_add=True, blank=False)
    file = models.FileField(upload_to='uploads/')

    @staticmethod
    def create(file):
        a=File(file)
        a.save()


