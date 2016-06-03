from django.contrib import admin
from .models import BNBUser, Property, Reservation, Review, View

admin.site.register(BNBUser)
admin.site.register(Property)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(View)
