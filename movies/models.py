from django.db import models
from photoes.models import Photo
from storage.models import Storage
from commontype.models import CommonType
from actors.models import Actor


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=255, verbose_name="Movie Name")
    movie_images = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Movie Images")
    provider = models.CharField(max_length=100, null=True, verbose_name="Movie Provider")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, verbose_name="Movie Storage Item")
    file_path = models.CharField(max_length=255, verbose_name="Movie File Path")
    movie_type = models.ForeignKey(CommonType, on_delete=models.CASCADE, verbose_name="Movie Type")
    actors = models.ManyToManyField(Actor, verbose_name="Actors of Movie")

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class MovieActorRef(models.Model):
#     movie_id = models.IntegerField()
#     actor_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Movie's actor"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "Movie id %d map to Actor id %d" % (self.movie_id, self.actor_id)
#
#
# class MovieSnapshotRef(models.Model):
#     movie_id = models.IntegerField()
#     snapshot_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Movie's Snapshot"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "Movie id %d map to Snapshot id %d" % (self.movie_id, self.snapshot_id)
#
#
# class MovieTypeRef(models.Model):
#     movie_id = models.IntegerField()
#     type_id = models.IntegerField()
#
#     class Meta:
#         verbose_name = "Movie's Type"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "Movie id %d map to Type id %d" % (self.movie_id, self.type_id)
