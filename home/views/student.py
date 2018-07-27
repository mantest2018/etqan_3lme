from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from ..models import Students, Tasks_Every_Day, Plan, Days, Tasks_Every_Weeks, Tasks_Every_Months
from .views import day_now, is_login
from ..form import Tasks_Every_Day_Form


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


def tasks_every_day(request, day_id=day_now(), student_id=''):

    if student_id == '':
        if request.session['user_type'] == 'student':
            student_id = request.session['member_id']
        else:
            return HttpResponseRedirect('/')

    if not is_login(request):
        return HttpResponseRedirect('/')
    try:
        s = Students.objects.get(pk=student_id)
        if request.session['user_type'] == 'student':
            if student_id != request.session['member_id']:
                admin = Students.objects.get(pk=request.session['member_id'])
                if not(admin.is_admin and admin.tracks==s.tracks):
                    return HttpResponseRedirect('/')
        if request.session['user_type'] == 'techer':
            if s.course.id != request.session['member_id']:
                return HttpResponseRedirect('/')
        report = Tasks_Every_Day.objects.get(student=student_id, day__id=day_id)
        fotmedit = Tasks_Every_Day_Form(request.POST or None, instance=report)
        is_save = ''
        if "POST" == request.method:
            fotmedit.save()
            is_save = 'تم حفظ البيانات'
        degree = "%.2f%%" % (100 * report.degree / 3)
        context = {'fotmedit': fotmedit, 'report': report, 'is_save': is_save, 'degree': degree}
    except(Plan.DoesNotExist, Students.DoesNotExist):
        raise Http404("الصفحة المطلوبة غير موجودة")
    except(Tasks_Every_Day.DoesNotExist):
        Student = Students.objects.get(pk=student_id)
        day = Days.objects.get(pk=day_id)
        updateData(Student, day)
        report = Tasks_Every_Day.objects.get(student=student_id, day__id=day_id)
        fotmedit = Tasks_Every_Day_Form(instance=report)
        context = {'fotmedit': fotmedit, 'report': report}
    return render(request, 'Student/Input_page.html', context)


def tasks_every_day_objects(showAllDay=False):
    if showAllDay == False:
        week = Days.objects.filter(id__lte=day_now()).latest('id').weeks
        return Tasks_Every_Day.objects.filter(day__id__lte=day_now(), day__weeks=week)
    else:
        return Tasks_Every_Day.objects.filter(day__id__lte=day_now())


def report_tasks_days(request, student_id=''):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if student_id == '':
            if request.session['user_type'] == 'techer':
                return HttpResponseRedirect('/')
            student_id = request.session['member_id']
        else:
            if request.session['user_type'] == 'student':
                if request.session['member_id'] != student_id:
                    return HttpResponseRedirect('/')
            if request.session['user_type'] == 'techer':
                if request.session['member_id'] != Students.objects.get(pk=student_id).tracks.id:
                    return HttpResponseRedirect('/')
        latest_list = ''
        student = Students.objects.get(pk=student_id)
        if request.session['user_type'] == 'student':
            latest_list = tasks_every_day_objects().filter(student=request.session['member_id']).order_by('day')
        if request.session['user_type'] == 'techer':
            latest_list = tasks_every_day_objects().filter(student=student_id,
                                                           student__tracks=request.session['member_id']).order_by(
                'day')

        context = {'latest_list': latest_list, 'student': student}
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'Student/report_tasks_days.html', context)


def tasks_every_week_objects():
    week = Tasks_Every_Day.objects.filter(day__id__lte=day_now()).latest('id').day.weeks
    return Tasks_Every_Weeks.objects.filter(weeks__id__lte=week.id)


def report_tasks_weeks(request, student_id=''):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if student_id == '':
            if request.session['user_type'] == 'techer':
                return HttpResponseRedirect('/')
            student_id = request.session['member_id']
        latest_list = ''
        if request.session['user_type'] == 'student':
            latest_list = tasks_every_week_objects().filter(student=request.session['member_id']).order_by('weeks')
        if request.session['user_type'] == 'techer':
            latest_list = tasks_every_week_objects().filter(student=student_id,
                                                            student__tracks=request.session['member_id']).order_by(
                'weeks')
        student = Students.objects.get(pk=student_id)
        context = {'latest_list': latest_list, 'student': student}
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'Student/report_tasks_weeks.html', context)


def tasks_every_month_objects():
    month = Tasks_Every_Day.objects.filter(day__id__lte=day_now())[0].day.weeks.months.id
    return Tasks_Every_Months.objects.filter(months__id__lte=month)


def report_tasks_months(request, student_id=''):
    try:
        if not is_login(request):
            return HttpResponseRedirect('/')
        if student_id == '':
            if request.session['user_type'] == 'techer':
                return HttpResponseRedirect('/')
            student_id = request.session['member_id']
        latest_list = ''
        if request.session['user_type'] == 'student':
            latest_list = tasks_every_month_objects().filter(student=request.session['member_id']).order_by('months')
        if request.session['user_type'] == 'techer':
            latest_list = tasks_every_month_objects().filter(student=student_id,
                                                             student__tracks=request.session['member_id']).order_by(
                'months')
        student = Students.objects.get(pk=student_id)
        context = {'latest_list': latest_list, 'student': student}
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'Student/report_tasks_months.html', context)


#    admin
def all_student(request):
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
        latest_list= Tasks_Every_Weeks.objects.filter(weeks__id=week.id,student__tracks=student.tracks)
        # latest_list = Students.objects.filter(tracks=student.tracks).order_by('student')
        context = {
            'latest_list': latest_list,
            'student': student,
            'week': week,
        }
    except(Students.DoesNotExist):
        raise Http404("Students does not exist")
    return render(request, 'Student/all_student.html', context)
