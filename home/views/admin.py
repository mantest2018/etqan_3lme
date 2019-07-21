from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months, Weeks, Months
from .views import day_now, is_login, is_administrator,day_now_object
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
# تقرير سنوي حسب الحلقة
def bilding_report_tasks_year(latest_list):
    from django.db.models import Sum, Avg , Q, CharField
    total = latest_list.aggregate(Avg('test'), Sum('total_all'), Sum('total'), Sum('count_present_all'),
                                  Sum('count_present'), Avg('degree'))
    # print(total)

    # total1 = latest_list.annotate(test__avg=Avg('test'), total_all__sum=Sum('total_all'), total__sum= Sum('total'),count_present_all__sum= Sum('count_present_all'),
    #                               count_present__sum=Sum('count_present'), degree__avg=Avg('degree'))
    # print(list(total1))
    latest_list_new = latest_list.values('months__name', 'months').annotate(test=Avg('test', filter=Q(is_stop=False),output_field=CharField()),
                                                                            total_all=Sum('total_all'),
                                                                            total=Sum('total'),
                                                                            count_present_all=Sum('count_present_all'),
                                                                            count_present=Sum('count_present'),
                                                                            degree=Avg('degree')).order_by('months')
    latest_list_new = list(latest_list_new)
    latest_list_new.append(total)
    return latest_list_new

def bilding_report_tasks_year_student(latest_list):
    from django.db.models import Sum, Avg , Q,CharField
    total = latest_list.aggregate(Avg('test'), Sum('total_all'), Sum('total'), Sum('count_present_all'),
                                  Sum('count_present'), Avg('degree'))
    latest_list_new = latest_list.values('student__student','student__tracks__name','months__name', 'months').annotate(test=Avg('test', filter=Q(is_stop=False),output_field=CharField()),
                                                                            total_all=Sum('total_all'),
                                                                            total=Sum('total'),
                                                                            count_present_all=Sum('count_present_all'),
                                                                            count_present=Sum('count_present'),
                                                                            degree=Avg('degree')).order_by('months')
    latest_list_new = list(latest_list_new)
    latest_list_new.append(total)
    return latest_list_new

def report_tasks_year(request):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if request.session['user_type'] != 'student':
            return HttpResponseRedirect('/')
        from .student import tasks_every_month_objects

        student_id = request.session['member_id']
        student = Students.objects.get(pk=student_id)
        if not student.is_admin:
            return HttpResponseRedirect('/')
        if request.path in ['/administrator/report_tasks_year/','/administrator/report_tasks_year/students/']:
            administrator=True
            latest_list = tasks_every_month_objects()
        else:
            administrator = False
            latest_list = tasks_every_month_objects().filter(student__tracks=student.tracks)

        latest_list=bilding_report_tasks_year(latest_list)

        students=False

        tracks_all={}
        if administrator:
            if request.path == '/administrator/report_tasks_year/students/':
                students = True
                from ..models import Tracks
                for student in Students.objects.all():
                    tracks_all[str(student.id)] = bilding_report_tasks_year_student(
                        tasks_every_month_objects().filter(student=student))
            else:
                from ..models import Tracks
                for tracks in Tracks.objects.all():
                    tracks_all[str(tracks.name)] = bilding_report_tasks_year(tasks_every_month_objects().filter(student__tracks=tracks))


        context = {'latest_list': latest_list,'students':students,'student': student ,'path_admin': 'students/','administrator':administrator,'tracks_all':tracks_all}
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
        # latest_list = Plan.objects.filter(tracks=student.tracks,day__weeks__months__semeste=day_now_object().weeks.months.semeste)

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
            for i in ['is_stop','task1', 'task2', 'task3']:
                if request.POST.get(i, '') != '':
                    if i =="is_stop":
                        count_stoping = Tasks_Every_Day.objects.filter(student=student.id, is_stop=True).count()
                        if count_stoping > 20:
                            if is_administrator(request)==False:
                                raise Http404('لا يمكن حفظ البيانات تم تجاوز عدد المرات المسموح بها في الاستئذان تواصل مع المشرف')

                    item.__dict__[i] = not item.__dict__[i]
                    item.save()
                    bo = item.__dict__[i]
            return HttpResponse(bo)
        except(Students.DoesNotExist, Tasks_Every_Weeks.DoesNotExist):
            raise Http404("Students does not exist")
    return HttpResponse("erorr")
