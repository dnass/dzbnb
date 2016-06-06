from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import BNBUser, Property, Reservation, Review, View

admin.site.register(Property)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(View)

class UserInline(admin.StackedInline):
    model = BNBUser
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
