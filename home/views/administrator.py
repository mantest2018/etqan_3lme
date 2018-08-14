from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months ,Weeks,Months
from .views import day_now, is_login

def report_tasks_months(request,month_id=''):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            return HttpResponseRedirect('/')
        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')
        month = Tasks_Every_Day.objects.filter(day__id__lte=day_now()).latest('id').day.weeks.months
        months= Months.objects.filter(id__lte=month.id)
        pathRoot=''
        if month_id != '':
            month = Months.objects.get(pk=month_id)
            pathRoot = '.'
        latest_list = Tasks_Every_Months.objects.filter(months=month)
        if request.method == 'POST':
            for key ,value in  request.POST.dict().items():
                try:
                    task=Tasks_Every_Months.objects.get(id=key)
                    task.test=value
                    task.save()
                except:
                    print(key)
        context = {
            'latest_list': latest_list,
            'student': student,
            'months':months,
            'month': month,
            'pathRoot':pathRoot,
            'path_admin':'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'administrator/report_tasks_months.html', context)