from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import datetime
from ..models import Students, Days ,Plan ,Intent
from django.db.models import Q

# Create your views here.


def day_now():
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
    return HttpResponseRedirect('/login')


def login(request):
    if "POST" == request.method:
        try:
            if request.POST['user_type'] == 'student':
                m = Students.objects.get(number_user=request.POST['id_user'])
                if m.password == request.POST.get("password", ""):
                    request.session['user_type'] = request.POST['user_type']
                    if m.is_admin:
                        request.session['admin']=None
                        if m.choice_text =='administrator':
                            request.session['administrator'] = None
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

def is_admin(request):
    if not is_login(request):
        return False
    student_id = request.session['member_id']
    student = Students.objects.get(pk=student_id)
    if  student.is_admin:
        return True
    return False

def is_administrator(request):
    return is_admin(request) and "administrator" in request.session


def logout(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    if "member_id" in request.session:
        del request.session['member_id']
    if "user_type" in request.session:
        del request.session['user_type']
    if "admin" in request.session:
        del request.session['admin']
    if "administrator" in request.session:
        del request.session['administrator']
    return HttpResponseRedirect('/')

import _thread

is_update_now=False
prossing=0

def proces_update():
    global is_update_now
    global prossing
    student=Students.objects.all()
    prossing=0
    n=0
    count=student.count()
    for item in student:
        item.save()
        prossing=n/count
        n = n + 1
    is_update_now = False
    pass


def update(request):
    global is_update_now
    global prossing

    if "POST" == request.method:
        if is_update_now == False:
            is_update_now = True
            _thread.start_new_thread(proces_update, ())

    context = {
        'prossing': prossing,
    }
    return render(request,'update.html',context)





def donload_Plan(request):
    if not is_admin(request):
        return HttpResponseRedirect('/')

    import csv
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="Plan.csv"'

    writer = csv.writer(response, delimiter=';')

    writer.writerow(['id', 'اليوم','التاريخ', 'الهدف', 'المقدار'])

    student_id = request.session['member_id']
    student = Students.objects.get(pk=student_id)

    for day_item in Days.objects.all():
        try:
            item = Plan.objects.get(tracks=student.tracks, day=day_item)

            if item.intent:
                 writer.writerow([day_item.id, day_item, day_item.date_hijri(), item.intent.id, item.amount])
        except Plan.DoesNotExist:
            writer.writerow([day_item.id, day_item, day_item.date_hijri(), '', ''])
    return response

def donload_intent(request):
    if not is_admin(request):
        return HttpResponseRedirect('/')

    import csv
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="intent.csv"'

    writer = csv.writer(response, delimiter=';')

    writer.writerow(['id', 'الهدف','المهمة1', 'المهمة2', 'المهمة3'])

    student_id = request.session['member_id']
    student = Students.objects.get(pk=student_id)

    for item in Intent.objects.all():
        writer.writerow([item.id, item.name, item.task1,item.task2,item.task3])
    return response




def upload_Plan(request):
    if not is_admin(request):
        return HttpResponseRedirect('/')
    data = {}
    if "GET" == request.method:
        return HttpResponseRedirect('/all_student')
        # return render(request, "myapp/upload_csv1.html", data)
    # if not GET, then proceed
    # try:
    import csv
    # file = request.FILES['Plan']
    # decoded_file = file.read().splitlines()
    # for item in decoded_file:
    #     item=item.decode('utf-8-sig')
    #
    # csv_file = request.FILES["Plan"]
    # file_data = csv_file.read().decode("utf-8")
    # file=file_data.replace('\r','')
    # file =   file1.replace('\ufeff1','')
    lines = request.FILES['Plan'].read().splitlines()
    # loop over the lines and save them in db. If error , store as string and then display
    student_id = request.session['member_id']
    student = Students.objects.get(pk=student_id)
    for line in lines:
        fields = line.decode('utf-8-sig').split(";")
        if fields[0] == 'id' or fields[0] == '':
            continue
        if fields[3] == '':
            continue
        try:
            id= int(fields[0])
        except ValueError:
            continue
        day_item = Days.objects.get(id=id)

        if day_item:
            try:
                if fields[3] != '':
                    intent = Intent.objects.get(id=int(fields[3]))
            except Plan.DoesNotExist:
                intent=None

            try:
                item = Plan.objects.get(tracks=student.tracks, day=day_item)
                item.intent=intent
                item.amount=fields[4]
                item.save()
            except Plan.DoesNotExist:
                plan=Plan(tracks=student.tracks,day=day_item,intent = intent ,amount = fields[4])
                plan.save()


    # except:
    #     print('erorr')

    return HttpResponseRedirect('/all_student')