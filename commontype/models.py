from django.db import models


# Create your models here.
class CommonType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Type Name")
    parent = models.ForeignKey('CommonType', verbose_name="Parent Type", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Common Type"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

