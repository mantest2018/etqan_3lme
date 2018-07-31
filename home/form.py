from django import forms
from django.db.models import Count

from .models import Plan
from .models import Tasks_Every_Day


# class CoursesForm(forms.ModelForm):
#     class Meta:
#         model = Courses
#         fields = ['name_course', 'phone_nemper']


class Tasks_Every_Day_Form(forms.ModelForm):
    task1 = forms.BooleanField(label='المهمة الأولى', required=False)
    task2 = forms.BooleanField(label='المهمة الثانية', required=False)
    task3 = forms.BooleanField(label='المهمة الثالثة', required=False)
    amount=False

    class Meta:
        model = Tasks_Every_Day
        fields = ['task1', 'task2', 'task3']

    def getAmount(self):
        return self.amount

    def __init__(self, *args, **kwargs):
        super(Tasks_Every_Day_Form, self).__init__(*args, **kwargs)

        try:
            plan = Plan.objects.get(day__id=self.instance.day.id, tracks__id=self.instance.student.tracks.id)
            self.amount = plan.amount
            for item in ['task1', 'task2', 'task3']:
                self.fields[item].help_text = plan.intent.__dict__[item]
        except Plan.DoesNotExist:
            pass




#
# class Demo_Form(forms.ModelForm):
#     present = forms.ModelChoiceField(label='الحضور', queryset=Present.objects.all())
#     number_pages = forms.FloatField(label='عدد الأوجه', required=False, min_value=0, max_value=100)
#     count_erorr = forms.IntegerField(label='الأخطاء واللحون', required=False, min_value=0, max_value=100)
#     count_alirt = forms.IntegerField(label='التنبيهات', required=False, min_value=0, max_value=100)
#     notes = forms.CharField(label='ملاحظات', required=False, widget=forms.Textarea)
#
#     class Meta:
#         model = Demo
#         fields = ['present', 'number_pages', 'count_erorr', 'count_alirt', 'notes']


# from django.forms import modelformset_factory
# Demo_Form_Set = modelformset_factory(Demo, fields=('present',))
