import datetime
from django import forms
from django.db import models


# Create your models here.
from django.db.models import Sum , Count


class Tracks(models.Model):
    name = models.CharField(max_length=200)
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
        return str(self.name) + '  ' +str(self.years)


class Weeks(models.Model):
    months = models.ForeignKey(Months, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + '  ' + str(self.months)


class Days(models.Model):
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    end_time = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)

    def __str__(self):
        return str(self.name) + '  ' + str(self.date_hijri() )

    def date_hijri(self):
        from library.umalqurra.hijri_date import HijriDate
        um = HijriDate(self.start_time)
        return  um.date_hijri()


class Plan(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return str(self.day )+ '  ' + str(self.tracks )+ '  ' + str(self.intent )+ '  ' +  str(self.amount)


class Students(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.DO_NOTHING)
    student = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    number_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)
    is_show = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return  str(self.student)



    def save(self, *args, **kwargs):
        super(Students, self).save(*args, **kwargs)
        for item in Days.objects.all():
            updateData(self, item)


def updateData(Student, day):
    try:
        Tasks_Every_Day.objects.get(student=Student, day=day)
    except Tasks_Every_Day.DoesNotExist:
        report = Tasks_Every_Day(student=Student, day=day)
        report.save()
    try:
        Tasks_Every_Weeks.objects.get(student=Student, weeks=day.weeks)
    except Tasks_Every_Weeks.DoesNotExist:
        report = Tasks_Every_Weeks(student=Student, weeks=day.weeks)
        report.save()
    try:
        Tasks_Every_Months.objects.get(student=Student, months=day.weeks.months)
    except Tasks_Every_Months.DoesNotExist:
        report = Tasks_Every_Months(student=Student, months=day.weeks.months)
        report.save()


class Tasks_Every_Day(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    task1 = models.BooleanField(default=False)
    task2 = models.BooleanField(default=False)
    task3 = models.BooleanField(default=False)
    is_stop = models.NullBooleanField(default=None, null=True)
    degree = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.student) + '  ' + str(self.day)

    def save(self, *args, **kwargs):
        total=0
        for item in ['task1','task2','task3']:
            if self.__dict__[item]:
                total += 1
        self.degree = total
        super(Tasks_Every_Day, self).save(*args, **kwargs)


class Tasks_Every_Weeks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student) + '  ' + str(self.weeks)

    def chpresent(self):
        if self.present:
            return 'checkboxtrue'
        else:
            return 'checkboxfalse'
    def total_all(self):
        return Tasks_Every_Day.objects.filter(student=self.student,day__weeks=self.weeks).aggregate(count=Count('id'))[
                   'count'] * 3

    def total(self):
        return Tasks_Every_Day.objects.filter(student=self.student,day__weeks=self.weeks).aggregate(sum=Sum('degree'))['sum']

    def tasks_Day(self):
        return Tasks_Every_Day.objects.filter(student=self.student,day__weeks=self.weeks)

class test_form(forms.Form):
    test = forms.FloatField(label='الإختبار', required=False, min_value=0, max_value=30)

class Tasks_Every_Months(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    months = models.ForeignKey(Months, on_delete=models.CASCADE)
    test = models.FloatField(default=0)

    def __str__(self):
        return str(self.student )+ '  ' + str(self.months)

    def total_all(self):
        return Tasks_Every_Day.objects.filter(student=self.student,day__weeks__months=self.months).aggregate(count=Count('id'))[
                   'count'] * 3

    def total(self):
        return Tasks_Every_Day.objects.filter(student=self.student,day__weeks__months=self.months).aggregate(sum=Sum('degree'))['sum']

    def count_present_all(self):
        return Tasks_Every_Weeks.objects.filter(student=self.student,weeks__months=self.months).aggregate(count=Count('id'))[
                   'count']

    def count_present(self):
        return Tasks_Every_Weeks.objects.filter(student=self.student,weeks__months=self.months,present='True').aggregate(count=Count('id'))[
                   'count']

    def degree(self):
        if self.total_all() ==0 or self.count_present_all()==0:
            return 'يوجد نقص في الإدخال'
        degree= 50 * (self.total()/self.total_all())+20*(self.count_present()/self.count_present_all())+self.test
        return "%.2f%%" %  degree



    def test_as(self):
        try:
            form = test_form(initial={'test': self.test})
            form['test'].html_name =  str(self.id)
            return form['test']
        except :
            return 'يوجد مشكلة تواصل مع المسؤول عن الموقع'

class Record(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    time = models.CharField(max_length=50, null=True, blank=True)
    working = models.CharField(max_length=250, null=True, blank=True)
    achievements = models.CharField(max_length=250, null=True, blank=True)
    Costs = models.CharField(max_length=250, null=True, blank=True)
    recommendations = models.CharField(max_length=250, null=True, blank=True)

