from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cast(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name='%(class)s_set')
    casts = models.ManyToManyField(Cast, related_name='%(class)s_set')
    poster_image = models.ImageField(upload_to='posters/')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Movie(BaseContent):
    pass


class Series(BaseContent):
    pass
