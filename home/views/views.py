from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from ..models import Students


def index(request):
    if is_login(request):
        if request.session['user_type'] == 'student':
            return render(request, 'home/index.html')

    #         # return tasks_every_day(request, day_now(), request.session['member_id'])
    #     if request.session['user_type'] == 'techer':
    #         return students(request, day_now())
    #
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

