from django.db import models
from commontype.models import CommonType
from photoes.models import Photo


# Create your models here.

class Actor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Actor Name")
    gender_choices = (
        (1, "Male"),
        (2, "Female")
    )
    sex = models.SmallIntegerField(choices=gender_choices, verbose_name="Actor Sex")
    country = models.CharField(max_length=50, verbose_name="Actor Country")
    description = models.TextField(verbose_name="Actor Description")
    thumb = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Actor thumb")
    commontype = models.ForeignKey(CommonType, on_delete=models.CASCADE, verbose_name="Actor Type")

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class ActorTypeRef(models.Model):
#     actor_id = models.IntegerField()
#     type_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Actor's type"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "Actor id %d map to type id %d" % (self.actor_id, self.type_id)
