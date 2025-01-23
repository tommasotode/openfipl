from django.db import models

class Performance(models.Model):
    Name = models.CharField(max_length=128)
    Sex = models.CharField(max_length=2)
    Event = models.CharField(max_length=4)
    Equipment = models.CharField(max_length=32)
    Age = models.IntegerField()
    Division = models.CharField(max_length=32)
    BodyweightKg = models.FloatField()
    WeightClassKg = models.CharField(max_length=4)
    BestSquatKg = models.FloatField()
    BestBenchKg = models.FloatField()
    BestDeadliftKg = models.FloatField()
    TotalKg = models.FloatField()
    Place = models.IntegerField()
    IPFGLPoints = models.FloatField()
    Country = models.CharField(max_length=64)
    Federation = models.CharField(max_length=32)
    Date = models.CharField(max_length=16)
    MeetName = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.Name} {self.IPFGLPoints}"