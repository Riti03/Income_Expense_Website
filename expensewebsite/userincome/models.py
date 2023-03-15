from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class UserIncome(models.Model):
    amount = models.FloatField()  # DECIMAL
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=266)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank = False)
    writer = models.CharField(max_length=255)
    publishedat = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Consulting(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    exp = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    scheduledat= models.CharField(max_length=255)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


