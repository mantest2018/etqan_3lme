from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months ,Weeks,Months
from .views import day_now, is_login
from ..form import Tasks_Every_Day_Form



#    admin
def students(request):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            return HttpResponseRedirect('/')
        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')
        latest_list = Students.objects.filter(tracks=student.tracks)
        context = {
            'latest_list': latest_list,
            'student': student,
            'path_admin': 'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'admin/students.html', context)



def report_tasks_weeks(request,week_id=''):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            return HttpResponseRedirect('/')
        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')
        week = Tasks_Every_Day.objects.filter(day__id__lte=day_now()).latest('id').day.weeks
        weeks=Weeks.objects.filter(id__lte=week.id)
        pathRoot = ''
        if week_id!='':
            week=Weeks.objects.get(pk=week_id)
            pathRoot = '.'
        latest_list= Tasks_Every_Weeks.objects.filter(weeks__id=week.id,student__tracks=student.tracks)
        context = {
            'latest_list': latest_list,
            'student': student,
            'week': week,
            'weeks':weeks,
           'pathRoot': pathRoot ,
            'path_admin':'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'admin/report_tasks_weeks.html', context)


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
        latest_list = Tasks_Every_Months.objects.filter(months=month,student__tracks=student.tracks)
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
    return render(request, 'admin/report_tasks_months.html', context)


def plan(request):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            return HttpResponseRedirect('/')
        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')

        latest_list = Plan.objects.filter(tracks=student.tracks)
        context = {
            'latest_list': latest_list,
            'student': student,
            'path_admin':'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'admin/plan.html', context)

def present(request):
    if "POST" == request.method:
        try:
            if not is_login(request):
                return HttpResponseRedirect('/')
            if request.session['user_type'] == 'techer':
                return HttpResponseRedirect('/')
            student_id = request.session['member_id']
            student = Students.objects.get(pk=student_id)
            if not student.is_admin:
                return HttpResponseRedirect('/')
            id = request.POST.get('present_id' ,'')
            item = Tasks_Every_Weeks.objects.get(id=id, student__tracks=student.tracks)
            item.present= not item.present
            item.save()
            return HttpResponse(item.present)
        except(Students.DoesNotExist , Tasks_Every_Weeks.DoesNotExist):
            raise Http404("Students does not exist")
    return HttpResponse("erorr")

def task(request):
    if "POST" == request.method:
        try:
            if not is_login(request):
                return HttpResponseRedirect('/')
            if request.session['user_type'] == 'techer':
                return HttpResponseRedirect('/')
            student_id = request.session['member_id']
            student = Students.objects.get(pk=student_id)
            if not student.is_admin:
                return HttpResponseRedirect('/')
            id = request.POST.get('task_id' ,'')
            item = Tasks_Every_Day.objects.get(id=id, student__tracks=student.tracks)
            bo='erorr'
            for i in ['task1','task2','task3']:
                if request.POST.get(i ,'')!='':
                    item.__dict__[i]=not item.__dict__[i]
                    item.save()
                    bo=item.__dict__[i]
            return HttpResponse(bo)
        except(Students.DoesNotExist , Tasks_Every_Weeks.DoesNotExist):
            raise Http404("Students does not exist")
    return HttpResponse("erorr")