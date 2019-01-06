from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months, Weeks, Months
from .views import day_now, is_login, is_administrator
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
        latest_list = Tasks_Every_Weeks.objects.filter(weeks__id=week.id, student__tracks=student.tracks)
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
    return render(request, 'admin/report_tasks_weeks.html', context)


def record(request, week_id=''):
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
        from ..models import Record
        from ..form import Record_Form

        if week_id == '':
            weeks_id = week.id
        else:
            weeks_id = week_id
        try:
            record = Record.objects.get(weeks_id=weeks_id, tracks=student.tracks)
        except Record.DoesNotExist:
            record = Record(weeks_id=weeks_id, tracks=student.tracks)

        record_Form = Record_Form(request.POST or None, instance=record)
        is_save = ''

        if "POST" == request.method:
            record_Form.save()
            is_save = 'تم حفظ البيانات'

        if week_id != '':
            week = Weeks.objects.get(pk=week_id)
            pathRoot = '.'
        latest_list = Tasks_Every_Weeks.objects.filter(weeks__id=week.id, student__tracks=student.tracks)
        context = {
            'is_save': is_save,
            'record_Form': record_Form,
            'latest_list': latest_list,
            'student': student,
            'week': week,
            'weeks': weeks,
            'pathRoot': pathRoot,
            'path_admin': 'students/',
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'admin/record.html', context)


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
        latest_list = Tasks_Every_Months.objects.filter(months=month, student__tracks=student.tracks)
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
    return render(request, 'admin/report_tasks_months.html', context)


def report_tasks_year(request):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] != 'student':
            return HttpResponseRedirect('/')
        from .student import tasks_every_month_objects
        from django.db.models import Sum ,Avg
        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')
        if request.path =='/administrator/report_tasks_year/':
            administrator=True
            latest_list = tasks_every_month_objects()
                # .order_by('months')
        else:
            administrator = False
            latest_list = tasks_every_month_objects().filter(student__tracks=student.tracks)
        latest_list_new={}
        total=latest_list.aggregate(Avg('test'), Sum('total_all'), Sum('total'), Sum('count_present_all'),Sum('count_present'),Avg('degree'))
        latest_list_new=latest_list.values('months__name','months').annotate(test = Avg('test'),total_all = Sum('total_all'),total = Sum('total'),count_present_all = Sum('count_present_all'),count_present = Sum('count_present'),degree = Avg('degree')).order_by('months')
        # test =
        # total_all =
        # total =
        # count_present_all =
        # count_present =
        # degree =
        # for item in latest_list_old:
        #     if total=={}:
        #         total={
        #             'total_all':item.total_all(),
        #             'total':item.total(),
        #             'count_present':item.count_present(),
        #             'test':item.test,
        #             'degree':item.degree(True),
        #             'n':1
        #         }
        #     else:
        #         total = {
        #             'total_all': total['total_all'] + item.total_all(),
        #             'total': total['total'] + item.total(),
        #             'count_present': total['count_present'] + item.count_present(),
        #             'test': total['test'] + item.test,
        #             'degree': total['degree'] + item.degree(True),
        #             'n': total['n']+1
        #         }
        #     if not latest_list_new.get(item.months.name)  :
        #         latest_list_new[item.months.name]={
        #             'total_all':item.total_all(),
        #             'total':item.total(),
        #             'count_present':item.count_present(),
        #             'test':item.test,
        #             'degree':item.degree(True),
        #             'n': 1
        #         }
        #     else:
        #         latest_list_new[item.months.name]={
        #             'total_all':latest_list_new[item.months.name]['total_all']+item.total_all(),
        #             'total':latest_list_new[item.months.name]['total']+item.total(),
        #             'count_present':latest_list_new[item.months.name]['count_present']+item.count_present(),
        #             'test':latest_list_new[item.months.name]['test']+item.test,
        #             'degree':latest_list_new[item.months.name]['degree']+item.degree(True),
        #             'n': latest_list_new[item.months.name]['n'] + 1,
        #         }
        # total['is_total']=True
        # latest_list_new['المجموع'] = total
        # for item in latest_list_new:
        #     latest_list_new[item]['degree']=latest_list_new[item]['degree']/latest_list_new[item]['n']
        print(total)

        context = {'latest_list': latest_list_new,'total':total, 'student': student ,'path_admin': 'students/','administrator':administrator}
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'admin/report_tasks_year.html', context)



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
            'path_admin': 'students/',
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
            id = request.POST.get('present_id', '')
            if is_administrator(request):
                item = Tasks_Every_Weeks.objects.get(id=id)
            else:
                item = Tasks_Every_Weeks.objects.get(id=id, student__tracks=student.tracks)
            print(item.present)
            if item.present== True:
                item.present = None
            elif item.present == None:
                item.present = False
            elif item.present == False:
                item.present = True
            else:
                return HttpResponse("erorr")
            item.save()
            return HttpResponse(item.present)
        except(Students.DoesNotExist, Tasks_Every_Weeks.DoesNotExist):
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
            id = request.POST.get('task_id', '')
            if not student.is_admin:
                item = Tasks_Every_Day.objects.get(id=id, student__id=student.id)
            else:
                if is_administrator(request):
                    item = Tasks_Every_Day.objects.get(id=id)
                else:
                    item = Tasks_Every_Day.objects.get(id=id, student__tracks=student.tracks)
            bo = 'erorr'
            for i in ['task1', 'task2', 'task3']:
                if request.POST.get(i, '') != '':
                    item.__dict__[i] = not item.__dict__[i]
                    item.save()
                    bo = item.__dict__[i]
            return HttpResponse(bo)
        except(Students.DoesNotExist, Tasks_Every_Weeks.DoesNotExist):
            raise Http404("Students does not exist")
    return HttpResponse("erorr")
