from django.contrib import admin
from .models import Account,NormalUser,BiteReport
from import_export.admin import ImportExportModelAdmin  
from import_export import resources
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )
    
admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Account)
admin.site.register(NormalUser)
admin.site.register(BiteReport)