import datetime

from django.db import models


# Create your models here.

class Tracks(models.Model):
    name = models.CharField(max_length=200)
    is_save = models.BooleanField(default=True)
    notes = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Intent(models.Model):
    name = models.CharField(max_length=200)
    task1 = models.CharField(max_length=50)
    task2 = models.CharField(max_length=50)
    task3 = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Years(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Months(models.Model):
    years = models.ForeignKey(Years, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name + '  ' + self.years)


class Weeks(models.Model):
    months = models.ForeignKey(Months, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name + '  ' + self.months + '  ' + self.years)


class Days(models.Model):
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    end_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)

    # id_demo = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.name + '  ' + self.weeks + '  ' + self.months + '  ' + self.years)


class Plan(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return str(self.day + '  ' + self.tracks + '  ' + self.intent + '  ' + self.tracks + '  ' + self.amount)


class Students(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.DO_NOTHING)
    student = models.CharField(max_length=200)
    phone_nemper = models.CharField(max_length=10)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    number_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)
    is_show = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student + '  ' + self.tracks)


class Tasks_Every_Day(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    is_task1 = models.BooleanField(default=False)
    is_task2 = models.BooleanField(default=False)
    is_task3 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student + '  ' + self.plan)


class Tasks_Every_Weeks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student + '  ' + self.weeks)


class Tasks_Every_Months(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    months = models.ForeignKey(Months, on_delete=models.CASCADE)
    test = models.FloatField(default=0)

    def __str__(self):
        return str(self.student + '  ' + self.months)
