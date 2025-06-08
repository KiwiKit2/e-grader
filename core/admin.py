from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (User, School, ClassYear, Subject, ProgramTerm,
                     Director, Teacher, Student, Parent, Grade, Attendance)

# User
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')

# Other models
admin.site.register(School)
admin.site.register(ClassYear)
admin.site.register(Subject)
admin.site.register(ProgramTerm)
admin.site.register(Director)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Grade)
admin.site.register(Attendance)
