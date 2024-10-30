from django.db import models

class Athletes(models.Model):
    Name = models.CharField(max_length=128)
    Sex = models.CharField(max_length=2)
    Event = models.CharField(max_length=3)
    Equipment = models.CharField(max_length=24)
    Division = models.CharField(max_length=32)
    WeightClassKg = models.CharField(max_length=4)
    TotalKg = models.FloatField()
    Federation = models.CharField(max_length=16)
    Date = models.CharField(max_length=24)
    MeetName = models.CharField(max_length=128)
