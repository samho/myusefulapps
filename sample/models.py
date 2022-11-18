from django.db import models


# Create your models here.
class Sample(models.Model):
    name = models.CharField(max_length=100)
    sample_txt = models.CharField(max_length=255)
    sample_id = models.IntegerField()

    class Meta:
        db_table = "sample"
        verbose_name = "Sample"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
