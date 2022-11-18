from django.db import models
from commontype.models import CommonType
from storage.models import Storage
from actors.models import Actor


# Create your models here.
class EBook(models.Model):
    name = models.CharField(max_length=50, verbose_name="EBook Name")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="EBook Storage")
    file_path = models.CharField(max_length=500, verbose_name="EBook File Path")
    ebook_type = models.ForeignKey(CommonType, verbose_name="EBook Type", on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, verbose_name="Actors of EBook")

    class Meta:
        verbose_name = "Ebooks"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#
#
# class EBookTypeRef(models.Model):
#     ebook_id = models.IntegerField()
#     type_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "EBook's type"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "EBook id: %d map to CommonType id %d" % (self.ebook_id, self.type_id)
#
#
# class EBookActorRef(models.Model):
#     ebook_id  = models.IntegerField()
#     actor_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "EBook's actor"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "EBook id: %d map to Actor id %d" % (self.ebook_id, self.actor_id)
