from django.db import models

# Create your models here.
class Img(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images', default='default.png')

    def __str__(self):
        return self.image.url