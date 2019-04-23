from django.contrib import admin
from .models import Tracks, Intent, Years, Months, Weeks, Days, Plan, Students, Tasks_Every_Day, Tasks_Every_Weeks, \
    Tasks_Every_Months, Record


# Register your models here.

class Tracks_Admin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Tracks


class Intent_Admin(admin.ModelAdmin):
    list_display = ['name', 'task1', 'task2', 'task3']

    class Meta:
        model = Intent


class Years_Admin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Years


class Months_Admin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Months


class Weeks_Admin(admin.ModelAdmin):
    list_display = ['__str__']

    class Meta:
        model = Weeks


class Days_Admin(admin.ModelAdmin):
    list_display = ['__str__', 'start_time', 'end_time']

    class Meta:
        model = Days


class Plan_Admin(admin.ModelAdmin):
    list_display = ['tracks', 'intent', 'day', 'amount']

    class Meta:
        model = Plan


admin.site.register(Tracks, Tracks_Admin)
admin.site.register(Intent, Intent_Admin)
admin.site.register(Years, Years_Admin)
admin.site.register(Months, Months_Admin)
admin.site.register(Weeks, Weeks_Admin)
admin.site.register(Days, Days_Admin)
admin.site.register(Plan, Plan_Admin)


class Students_Admin(admin.ModelAdmin):
    list_display = ['student','get_date_registr', 'tracks', 'is_admin','get_date_deleted', 'choice_text']

    class Meta:
        model = Students

@admin.register(Tasks_Every_Day)
class Tasks_Every_Day_Admin(admin.ModelAdmin):
    list_display = ['student','day', 'day__start_time', 'day__weeks','day__weeks__months']
    search_fields = ('student__student',)
    list_filter = ('student', 'day__weeks','day__weeks__months')



admin.site.register(Students, Students_Admin)
# admin.site.register(Tasks_Every_Day,Tasks_Every_Day_Admin)
admin.site.register(Tasks_Every_Weeks)
admin.site.register(Tasks_Every_Months)
admin.site.register(Record)
