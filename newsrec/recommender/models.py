# in recommender/models.py
from django.db import models

class Article(models.Model):
    headline = models.CharField(max_length=255)
    rowid = models.IntegerField()
    article_link = models.URLField()

    def __str__(self):
        return self.headline
class Meta:
        db_table = 'custom_table'