from django.db import models
from commontype.models import CommonType


# Create your models here.
class Storage(models.Model):
    name = models.CharField(max_length=50, verbose_name="Storage Name")
    commontype = models.OneToOneField(CommonType, on_delete=models.CASCADE, verbose_name="Storage Type")
    size = models.FloatField(null=True, verbose_name="Storage Size")

    class Meta:
        verbose_name = "Storage"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
