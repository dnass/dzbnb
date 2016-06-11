from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'), # ex: /dzbnb/
    url(r'^reservation/(?P<reservation_id>[0-9]+)/approve/$', views.approve_reservation, name='approve_reservation'), # ex: /dzbnb/reservation/123/approve
    url(r'^property/(?P<propertie_id>[0-9]+)/$', views.propertie, name='property_details'), # ex: /dzbnb/property/123
    url(r'^property/(?P<propertie_id>[0-9]+)/request/$', views.request_reservation, name='request_reservation'), # ex: /dzbnb/property/123/request
    url(r'^property/(?P<propertie_id>[0-9]+)/edit/$', views.edit_property, name='edit_property'), # ex: /dzbnb/property/123/edit
    url(r'^property/(?P<propertie_id>[0-9]+)/hide/$', views.hide_property, name='hide_property'), # ex: /dzbnb/property/123/hide
    url(r'^property/(?P<propertie_id>[0-9]+)/unhide/$', views.unhide_property, name='unhide_property'), # ex: /dzbnb/property/123/unhide
    url(r'^property/(?P<propertie_id>[0-9]+)/review/$', views.review_property, name='review_property'), # ex: /dzbnb/property/123/review
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user_details, name='user_details'), # ex: /dzbnb/user/123
]
