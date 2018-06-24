import datetime

from django.db import models


# Create your models here.

class Tracks(models.Model):
    name = models.CharField(max_length=200)
    is_save = models.BooleanField(default=True)
    notes = models.CharField(max_length=250, null=True, blank=True)


class Intent(models.Model):
    name = models.CharField(max_length=200)
    task1 = models.CharField(max_length=50)
    task2 = models.CharField(max_length=50)
    task3 = models.CharField(max_length=50)


class Days(models.Model):
    name_day = models.CharField(max_length=50)
    start_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    end_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    id_demo = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.name_day)


class Plan(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)


class Students(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    student = models.CharField(max_length=200)
    phone_nemper = models.CharField(max_length=10)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    number_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)
    is_admin = models.BooleanField(default=True)
