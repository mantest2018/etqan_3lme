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
                    if m.is_admin:
                        request.session['admin']=None
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

def logout(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    if "member_id" in request.session:
        del request.session['member_id']
    if "user_type" in request.session:
        del request.session['user_type']
    if "admin" in request.session:
        del request.session['admin']
    return HttpResponseRedirect('/')

def update(request):
    for item in Students.objects.all():
        item.save()
    return HttpResponse("تم")

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
        item=Plan.objects.filter(tracks=student.tracks,day=day_item)
        if item:
            writer.writerow([day_item.id, day_item , day_item.date_hijri() ,item.intent, item.amount])
        else:
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
    csv_file = request.FILES["Plan"]
    file_data = csv_file.read().decode("utf-8-sig")

    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    student_id = request.session['member_id']
    student = Students.objects.get(pk=student_id)
    for line in lines:
        fields = line.split(";")

        # try:
        if fields[0]=='id':
            continue
        id= str(fields[0])
        id = int(id)
        # except ValueError:
        #     print(fields[0])
        #     continue
        day_item = Days.objects.filter(id=id)
        if day_item:
            item = Plan.objects.filter(tracks=student.tracks, day=day_item)
            print(item)
            if item:
                item.intent=fields[3]
                item.amount=fields[4]
                item.save()
            else:
                plan=Plan(tracks=student.tracks,day=day_item,intent = fields[3],amount = fields[4])
                plan.save()


    # except:
    #     print('erorr')

    return HttpResponseRedirect('/all_student')