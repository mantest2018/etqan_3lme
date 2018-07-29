from django.urls import path, re_path
from .views import views,student

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
    path('all_student/', student.all_student, name='all_student'),

    path('present/', student.present, name='present'),


]
