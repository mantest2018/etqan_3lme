from django.http import HttpResponse
from django.shortcuts import render

from home.models import Students


import _thread

is_update_now=False
count=0
n = 0
def proces_update():
    global is_update_now
    global prossing
    global n
    global count
    students = Students.objects.all()
    count = students.count()
    n = 0
    is_update_now=True
    print("start update")
    for student in students:
        print(student)
        student.save()
        n = n + 1
    print("fish update")

    count =0
    n = 0
    is_update_now=False

def update(request):

    global count
    global n

    try:
        if count == 0:
            _thread.start_new_thread(proces_update, ())
    except:
        print("Error: unable to start thread")

    context = {
        'count': count,
    }
    return render(request,'update.html',context)




class Middleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if is_update_now:
            global n
            global count
            context = {
                'count': count,
                'n':n
            }
            return render(request, 'update.html', context)


        response = self.get_response(request)

        return response


