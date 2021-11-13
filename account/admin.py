from django.contrib import admin
from .models import User
from import_export.admin import ImportExportModelAdmin
from .resource import UserResource


class UsersAdmin(ImportExportModelAdmin):
    resource_class = UserResource


admin.site.register(User, UsersAdmin)





