from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months, Weeks, Months, Tracks
from .views import day_now, is_login


def report_tasks_months(request, month_id=''):
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
        months = Months.objects.filter(id__lte=month.id)
        pathRoot = ''
        if month_id != '':
            month = Months.objects.get(pk=month_id)
            pathRoot = '.'
        latest_list = Tasks_Every_Months.objects.filter(months=month)
        if request.method == 'POST':
            pos=request.POST
            from library.mylib import parse_multi_form
            for key, value in parse_multi_form(pos)['tast_month'].items():
                try:
                    task = Tasks_Every_Months.objects.get(id=key)
                    task.test = float(value['test'])
                    if value.get('is_stop')== 'on':
                        task.is_stop = True
                    else:
                        task.is_stop = False
                    task.save()
                except:
                    print("erorr")

        context = {
            'latest_list': latest_list,
            'student': student,
            'months': months,
            'month': month,
            'pathRoot': pathRoot,
            'path_admin': 'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'administrator/report_tasks_months.html', context)


def report_tasks_weeks(request, week_id=''):
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
        weeks = Weeks.objects.filter(id__lte=week.id)
        pathRoot = ''
        if week_id != '':
            week = Weeks.objects.get(pk=week_id)
            pathRoot = '.'

        latest_list = []
        i = 0
        for list in Tracks.objects.all():
            latest_list.append([])
            latest_list[i].extend(Tasks_Every_Weeks.objects.filter(weeks__id=week.id, student__tracks=list))
            i = i + 1
        context = {
            'latest_list': latest_list,
            'student': student,
            'week': week,
            'weeks': weeks,
            'pathRoot': pathRoot,
            'path_admin': 'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'administrator/report_tasks_weeks.html', context)


def record(request, week_id, tracks_id):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            return HttpResponseRedirect('/')
        student_id = request.session['member_id']
        administrator = Students.objects.get(pk=student_id)
        if not administrator.is_admin:
            return HttpResponseRedirect('/')
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')

        week = Tasks_Every_Day.objects.filter(day__id__lte=day_now()).latest('id').day.weeks
        weeks = Weeks.objects.filter(id__lte=week.id)
        pathRoot = ''
        from ..models import Record, Tracks
        from ..form import Record_Form
        weeks_id = week_id
        tracks = Tracks.objects.get(id=tracks_id)
        try:
            record = Record.objects.get(weeks_id=weeks_id, tracks=tracks_id)
        except Record.DoesNotExist:
            record = Record(weeks_id=weeks_id, tracks=tracks)

        record_Form = Record_Form(request.POST or None, instance=record)
        is_save = ''

        if "POST" == request.method:
            record_Form.save()
            is_save = 'تم حفظ البيانات'

        if week_id != '':
            week = Weeks.objects.get(pk=week_id)
            pathRoot = '.'
        latest_list = Tasks_Every_Weeks.objects.filter(weeks__id=week.id, student__tracks=tracks_id)
        context = {
            'is_save': is_save,
            'record_Form': record_Form,
            'latest_list': latest_list,
            'tracks': tracks,
            'week': week,
            'pathRoot': pathRoot,
            'path_admin': 'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'administrator/record.html', context)
