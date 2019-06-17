import datetime
from django import forms
from django.db import models

# Create your models here.
from django.db.models import Sum, Count


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
    test_is_stop = models.NullBooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.name) + '  ' + str(self.years)


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
        return str(self.name) + '  ' + str(self.date_hijri())

    def date_hijri(self):
        from library.umalqurra.hijri_date import HijriDate
        um = HijriDate(self.start_time)
        return um.date_hijri()


class Plan(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return str(self.day) + '  ' + str(self.tracks) + '  ' + str(self.intent) + '  ' + str(self.amount)


class Students(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.DO_NOTHING)
    student = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    date_registr = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)
    number_user = models.IntegerField(default=0)
    password = models.CharField(max_length=8)
    is_show = models.BooleanField(default=True)
    date_deleted = models.DateTimeField(default=None, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    settings = models.CharField(default='{}', max_length=350, null=True, blank=True)


    def __str__(self):
        return str(self.student)

    def get_date_registr(self):
        from library.umalqurra.hijri_date import HijriDate
        date_hijri = HijriDate( self.date_registr)
        return date_hijri.date_hijri()

    def get_date_deleted(self):
        from library.umalqurra.hijri_date import HijriDate
        if self.date_deleted:
            date_hijri = HijriDate(self.date_deleted)
            return date_hijri.date_hijri()
        else:
            return "-------"

    def set_date_remove(self, date_remove):
        if self.settings == '{}':
            self.full_settings()
        import json
        setting = json.loads(self.settings)
        setting['date_remove'] = date_remove
        self.settings = json.dumps(setting)
        self.save()
        pass

    def get_date_remove(self):
        if self.settings == '{}':
            self.full_settings()
        import json
        setting = json.loads(self.settings).get('date_remove')
        return setting


    def full_settings(self):
        import json
        setting = {}
        if self.settings == '{}':
            setting['last_change'] = datetime.datetime.now().strftime("%Y-%m-%d %X")
        else:
            setting = json.loads(self.settings)
            if not 'last_change' in setting:
                setting['last_change'] = datetime.datetime.now().strftime("%Y-%m-%d %X")
        self.settings = json.dumps(setting)
        pass

    def save(self, *args, **kwargs):
        self.full_settings()
        super(Students, self).save(*args, **kwargs)
        if self.is_show == False and not self.date_deleted == None :
            from django.db.models import Q
            for item in Days.objects.filter(Q(start_time__gte=self.date_registr)  & Q(start_time__lt=self.date_deleted) ):
                updateData(self, item)
            Tasks_Every_Day.objects.filter(student=self,day__start_time__gte=self.date_deleted,task1=False,task2=False,task3=False,is_stop=False).delete()
        else:
            Tasks_Every_Day.objects.filter(student=self,day__start_time__lt=self.date_registr, task1=False, task2=False,
                                           task3=False).delete()


            for item in Days.objects.filter(start_time__gte=self.date_registr):
                updateData(self, item)

        for tasks in Tasks_Every_Weeks.objects.filter(student=self):
            if Tasks_Every_Day.objects.filter(student=self, day__weeks=tasks.weeks).count() == 0:
                tasks.delete()
            else:
                tasks.save()

        for tasks in Tasks_Every_Months.objects.filter(student=self):
            if Tasks_Every_Weeks.objects.filter(student=self, weeks__months=tasks.months).count() == 0:
                tasks.delete()
            else:
                tasks.save()




def updateData(Student, day):
    try:
        report =Tasks_Every_Day.objects.get(student=Student, day=day)
    except Tasks_Every_Day.DoesNotExist:
        report = Tasks_Every_Day(student=Student, day=day)
    report.save()



class Tasks_Every_Day(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)
    task1 = models.BooleanField(default=False)
    task2 = models.BooleanField(default=False)
    task3 = models.BooleanField(default=False)
    is_stop = models.NullBooleanField(default=False, null=True, blank=True)
    degree = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.student) + '  ' + str(self.day)

    def save(self, *args, **kwargs):
        total = 0
        if self.is_stop == "":
            self.is_stop = None
        for item in ['task1', 'task2', 'task3']:
            if self.__dict__[item]:
                total += 1
        self.degree = total
        super(Tasks_Every_Day, self).save(*args, **kwargs)
        try:
            report=Tasks_Every_Weeks.objects.get(student=self.student,weeks=self.day.weeks)
        except Tasks_Every_Weeks.DoesNotExist:
            report = Tasks_Every_Weeks(student=self.student,weeks=self.day.weeks)
        report.save()


class Tasks_Every_Weeks(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    present = models.NullBooleanField(default=False)
    total_all = models.FloatField(default=0,null=True, blank=True)
    total = models.FloatField(default=0,null=True, blank=True)


    def __str__(self):
        return str(self.student) + '  ' + str(self.weeks)

    def chpresent(self):
        if self.present:
            return 'checkboxtrue'
        if self.present == None:
            return "checkboxnull"
        else:
            return 'checkboxfalse'

    def __setAll(self,tasks_every_day):

        self.total_all = tasks_every_day.exclude(is_stop=True).aggregate(count=Count('id'))[
                   'count'] * 3
        self.total=tasks_every_day.exclude(is_stop=True).aggregate(sum=Sum('degree'))[
            'sum']

    def tasks_Day(self):
        return Tasks_Every_Day.objects.filter(student=self.student, day__weeks=self.weeks)


    def save(self, *args, **kwargs):
        tasks_every_day = Tasks_Every_Day.objects.filter(student=self.student, day__weeks=self.weeks)
        if tasks_every_day:
            self.__setAll(tasks_every_day)
            super(Tasks_Every_Weeks, self).save(*args, **kwargs)
            try:
                report =Tasks_Every_Months.objects.get(student=self.student, months=self.weeks.months)
            except Tasks_Every_Months.DoesNotExist:
                report = Tasks_Every_Months(student=self.student, months=self.weeks.months)
            report.save()
        else:
            self.delete()


class test_form(forms.Form):
    test = forms.FloatField(label='الإختبار', required=False, min_value=0, max_value=30)

class is_stop_form(forms.Form):
    is_stop = forms.BooleanField(label='متوقف', required=False)


class Tasks_Every_Months(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    months = models.ForeignKey(Months, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    total_all=models.FloatField(default=0)
    total=models.FloatField(default=0)
    count_present_all=models.FloatField(default=0)
    count_present=models.FloatField(default=0)
    degree=models.FloatField(default=None,null=True, blank=True)
    is_stop = models.NullBooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return str(self.student) + '  ' + str(self.months)

    def __setAll(self,tasks_every_day):
        # self.tasks_every_day= Tasks_Every_Day.objects.filter(student=self.student, day__weeks__months=self.months)
        tasks_every_day=tasks_every_day.exclude(is_stop=True)


        self.tasks_every_week=Tasks_Every_Weeks.objects.filter(student=self.student, weeks__months=self.months)
        if tasks_every_day:
            self.total_all= tasks_every_day.aggregate(
                count=Count('id'))[
                       'count'] * 3
            self.total = tasks_every_day.aggregate(
                sum=Sum('degree'))['sum']
        else:
            self.total_all=0
            self.total =0
        if self.tasks_every_week:
            from django.db.models import  Q, CharField
            self.count_present_all = self.tasks_every_week.exclude(present=None).aggregate(count=Count('id'))[
                'count']

            self.count_present = self.tasks_every_week.filter(present='True').aggregate(
                count=Count('id'))[
                'count']
        else:
            self.count_present_all =0
            self.count_present =0

        if self.total_all == 0 or self.count_present_all == 0:
            if self.count_present_all == 0 :
                if self.months.test_is_stop or self.is_stop:
                    self.degree = 100 * (self.total / self.total_all)
                else:
                    self.degree = 70 * (self.total / self.total_all) + self.test
            else:
                self.degree =None
        else:
            if self.months.test_is_stop or self.is_stop:
                self.degree =  70 * (self.total / self.total_all) + 30 * (
                    self.count_present / self.count_present_all)
            else:
                self.degree =  50 * (self.total / self.total_all) + 20 * (
                    self.count_present / self.count_present_all) + self.test


    def is_stop_as(self):
        try:
            form = is_stop_form(initial={'is_stop': self.is_stop})
            form['is_stop'].html_name = "tast_month["+str(self.id)+"][is_stop]"
            return form['is_stop']
        except:
            return 'يوجد مشكلة تواصل مع المسؤول عن الموقع'

    def test_as(self):
        try:
            form = test_form(initial={'test': self.test})
            form['test'].html_name = "tast_month["+str(self.id)+"][test]"
            return form['test']
        except:
            return 'يوجد مشكلة تواصل مع المسؤول عن الموقع'

    def save(self, *args, **kwargs):
        # self.__setAll()
        super(Tasks_Every_Months, self).save(*args, **kwargs)
        tasks_every_day = Tasks_Every_Day.objects.filter(student=self.student, day__weeks__months=self.months)
        if tasks_every_day:
            self.__setAll(tasks_every_day)
            super(Tasks_Every_Months, self).save(*args, **kwargs)
        else:
            self.delete()



class Record(models.Model):
    tracks = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    weeks = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    day = models.ForeignKey(Days,blank=True, null=True, on_delete=models.CASCADE)
    other = models.CharField(max_length=50, null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)
    working = models.CharField(max_length=250, null=True, blank=True)
    achievements = models.CharField(max_length=250, null=True, blank=True)
    Costs = models.CharField(max_length=250, null=True, blank=True)
    recommendations = models.CharField(max_length=250, null=True, blank=True)
