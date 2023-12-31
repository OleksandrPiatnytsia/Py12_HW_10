from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=200)
    born_date = models.CharField(max_length=120)
    born_location = models.CharField(max_length=120)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.name


class Quot(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    quot = models.TextField()
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(auto_now_add=True)
