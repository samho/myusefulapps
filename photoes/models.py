from django.db import models
from commontype.models import CommonType


# Create your models here.
class Photo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Photo File Name")
    ext = models.CharField(max_length=10, verbose_name="Photo File Extend")
    path = models.CharField(max_length=255, verbose_name="Photo File Path")
    commontype = models.ForeignKey(CommonType, verbose_name="Photo Type", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class PhotoTypeRef(models.Model):
#     photo_id = models.IntegerField()
#     type_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Photo's type"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "Photo id %d map to Type id %d" % (self.photo_id, self.type_id)