from django.urls import path, re_path
from .views import views,student,admin

urlpatterns = [
    # home
    re_path(r'^$', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),

    # student
    path('report_tasks_days/', student.report_tasks_days, name='report_tasks_days'),
    path('report_tasks_weeks/', student.report_tasks_weeks, name='report_tasks_weeks'),
    path('report_tasks_months/', student.report_tasks_months, name='report_tasks_months'),


    # student and techer
    path('student/<int:student_id>/tasks_day/<int:day_id>/', student.tasks_every_day, name='tasks_every_day'),

    # student admin
    path('plan/', admin.plan, name='plan'),
    path('students/', admin.students, name='students'),
    # path('students/report_tasks_days/', admin.report_tasks_days, name='report_tasks_days'),
    path('students/report_tasks_weeks/', admin.report_tasks_weeks, name='report_tasks_weeks'),
    path('students/report_tasks_weeks/<int:week_id>/', admin.report_tasks_weeks, name='report_tasks_weeks'),
    path('students/report_tasks_months/', admin.report_tasks_months, name='report_tasks_months'),
    path('students/report_tasks_months/<int:month_id>/', admin.report_tasks_months, name='report_tasks_months'),


    path('present/', admin.present, name='present'),

    #     csv   donlond and upload
    path('upload_Plan/', views.upload_Plan, name='upload_Plan'),
    path('donload_Plan/', views.donload_Plan, name='donload_Plan'),
    path('donload_intent/', views.donload_intent, name='donload_intent'),




]
