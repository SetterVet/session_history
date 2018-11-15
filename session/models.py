from django.db import models

# Create your models here.
class CSVFile(models.Model):
    title = models.CharField(verbose_name='title',default="default", max_length=100)
    file = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.title


class Comment(models.Model):
    file=models.ForeignKey(CSVFile, related_name='CSV_file', on_delete=models.CASCADE)
    bad_day=models.DateField()
    comm=models.TextField()


