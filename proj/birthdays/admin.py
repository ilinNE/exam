from django.contrib import admin
from birthdays.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)
