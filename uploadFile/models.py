from django.db import models


# Create your models here.
class NBA(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=100, null=True)
    rating = models.IntegerField(null=True)
    jersey = models.CharField(max_length=10,null=True)
    team = models.CharField(max_length=100,null=True)
    position = models.CharField(max_length=10,null=True)
    b_day = models.CharField(max_length=15,null=True)
    height = models.CharField(max_length=15,null=True)
    weight = models.CharField(max_length=100,null=True)
    salary = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    draft_year = models.IntegerField(null=True)
    draft_round = models.CharField(max_length=20,null=True)
    draft_peak = models.CharField(max_length=20,null=True)
    college = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=10,null=True)
