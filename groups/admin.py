from django.contrib import admin
from . import models

# Register your models here.
# TabularInline class,this basically allows the user to utilize the admin interface
# in the website with the ability to edit models in the same page as the parent model
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)
