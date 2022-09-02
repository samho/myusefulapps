from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class User(models.Model):

    username = models.CharField('User Name', max_length=50)
    password = models.CharField('Password', max_length=255)
    create_at = models.DateField("Create Date", auto_now_add=True)
    update_at = models.DateField("Update Date", auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User Name"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)

    def is_valid(self, password):
        return check_password(password, self.password)

