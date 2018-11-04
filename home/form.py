from django import forms
from django.db.models import Count

from .models import Plan,Tasks_Every_Day,Days,Record



# class CoursesForm(forms.ModelForm):
#     class Meta:
#         model = Courses
#         fields = ['name_course', 'phone_nemper']

CHOICES = (
    (None, "مستمر"),
    (True, "متوقف")
)

class Tasks_Every_Day_Form(forms.ModelForm):
    task1 = forms.BooleanField(label='المهمة الأولى', required=False)
    task2 = forms.BooleanField(label='المهمة الثانية', required=False)
    task3 = forms.BooleanField(label='المهمة الثالثة', required=False)
    is_stop=forms.ChoiceField(choices=CHOICES,
        label='الحالة',
        required=False)
    # is_stop = forms.NullBooleanField(label='الحالة', required=False)
    amount=False

    class Meta:
        model = Tasks_Every_Day
        fields = ['task1', 'task2', 'task3','is_stop']

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


class Record_Form(forms.ModelForm):
    day = forms.ModelChoiceField(label='اليوم',queryset=Days.objects.none(),required=False)
    other = forms.CharField(label='آخر', required=False, max_length=50)
    time = forms.CharField(label='الزمن', required=False,max_length=50)
    working = forms.CharField(label='أعمال الجلسة', required=False, widget=forms.Textarea,max_length=250)
    achievements =  forms.CharField(label='المنجزات', required=False, widget=forms.Textarea,max_length=250)
    Costs = forms.CharField(label='التكاليف القادمة', required=False, widget=forms.Textarea,max_length=250)
    recommendations = forms.CharField(label='التوصيات', required=False, widget=forms.Textarea,max_length=250)

    def __init__(self,  *args, **kwargs):

        super(Record_Form, self).__init__(*args, **kwargs)
        self.fields['day'].queryset=Days.objects.filter(weeks__id=self.instance.weeks.id)

    class Meta:
        model = Record
        exclude=['weeks','tracks']


