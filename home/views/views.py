from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import datetime
from ..models import Students, Days
from django.db.models import Q

# Create your views here.


def day_now():
    # # print() datetime.datetime(2018, 5,  30, 6, 0, 2, 423063) datetime.datetime.now()
    t = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    return Days.objects.filter(Q(start_time__lte=t) | Q(id=1)).latest('id').id


def index(request):
    if is_login(request):
        if request.session['user_type'] == 'student':
            from .student import tasks_every_day
            return  tasks_every_day(request, day_now(), request.session['member_id'])
        if request.session['user_type'] == 'techer':
           return  print('**********************************')
            # return students(request, day_now())

    # last_day = Reports_all_days.objects.filter(id_demo=True, id__lt=day_now()).latest('id')
    # tasks = Tasks_every_day.objects.filter(reports_all_days__id__lte=last_day.id)
    # context = dict(
    #     number_pages=tasks.aggregate(sum=Sum('number_pages'))['sum'],
    #     link=tasks.aggregate(sum=Sum('link'))['sum']+tasks.aggregate(sum=Sum('review'))['sum'],
    #     last_day=last_day,
    # )
    # csrfContext = RequestContext(request)
    return HttpResponseRedirect('/login')


def login(request):
    if "POST" == request.method:
        try:
            if request.POST['user_type'] == 'student':
                m = Students.objects.get(number_user=request.POST['id_user'])
                if m.password == request.POST.get("password", ""):
                    request.session['user_type'] = request.POST['user_type']
                    request.session['member_id'] = m.id
                    request.session.set_test_cookie()
                    return HttpResponseRedirect('/')
            elif request.POST['user_type'] == 'techer':
                print('techer')
                # m = Courses.objects.get(numper_user=request.POST['id_user'])
                # if m.password == request.POST.get("password", ""):
                #     request.session['user_type'] = request.POST['user_type']
                #     request.session['member_id'] = m.id
                #     request.session.set_test_cookie()
                #     return HttpResponseRedirect('/')
        except: #(Courses.DoesNotExist, Students.DoesNotExist):
            erorr_user = 'أسم المستخدم أو كلمة المرور غير صحيحة'
            context = {'erorr_user': erorr_user}
            return render(request, 'login.html', context)
    # if request.session.test_cookie_worked():
    #     return students(request, request.session['member_id'])
    return render(request, 'login.html')

def is_login(request):
    return request.session.test_cookie_worked() and "member_id" in request.session

def logout(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    if "member_id" in request.session:
        del request.session['member_id']
    if "user_type" in request.session:
        del request.session['user_type']
    return HttpResponseRedirect('/')

def update(request):
    for item in Students.objects.all():
        item.save()
    return HttpResponse("تم")