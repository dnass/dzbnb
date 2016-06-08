from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg, Count



def homepage(request):
    if request.user.is_authenticated():
        recently_added_properties = Propertie.objects.order_by('-creation_date')[:10]
        reservation_requests = Reservation.objects.filter(propertie__owner__user_id=request.user.id).filter(approved=False).order_by('-start_date')
        context = {
            'bnbuser': BNBUser.objects.filter(user__id=request.user.id)[0],
            'recently_added_properties': recently_added_properties,
            'reservation_requests': reservation_requests,
        }
        return render(request, 'bnb/homepage.html', context)
    else:
        context = {'return_page': 'homepage'}
        return render(request, 'bnb/login.html', context)

def approve_reservation(request, reservation_id):
    try:
        r = Reservation.objects.get(pk=reservation_id)
        if request.user.is_authenticated() and (r.propertie.owner.user == request.user or request.user.is_superuser):
            if r.approved:
                warning = "It had been approved, though."
            else:
                warning = ""
                r.approved = True
                r.save()
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        # invalid reservation_id
        return HttpResponseNotFound(_('Reservation does not exist.'))
    except PermissionDenied:
        # user is not authrised to approve the reservation
        return HttpResponseForbidden(_('Permission Denied.'))
    except:
        # unexpected error
        return HttpResponse(_('An unexpected error occured.'))
    else:
        # all code excuted which means approve action successful
        return HttpResponse(_('Reservation [{}] is approved. {}'.format(reservation_id, warning)))

def propertie(request, propertie_id):
    try:
        p = Propertie.objects.annotate(average_rating=Avg('review__rating'), rating_count=Count('review')).get(pk=propertie_id)
        if p.hidden and not request.user.is_superuser:
            raise ObjectDoesNotExist
        else:
            
            context = {
                'p': p,
                'show_reservation_form': p.owner.user != request.user,
                'show_admin_links': request.user.is_superuser or p.owner.user == request.user,
                'requested_by': request.user.id,
                'reviews': Review.objects.filter(propertie__owner__id=p.owner.id).filter(hidden=False)
            }
    except ObjectDoesNotExist:
        return HttpResponseNotFound(_('Property not found'))
    except:
        # unexpected error
        return HttpResponse(_('An unexpected error occured.'))
    else:
        return render(request, 'bnb/property.html', context)

def request_reservation(request, propertie_id):
    #request.POST.get('start_date')
    #request.POST.get('end_date')
    return HttpResponseNotFound('to be coded.')

def edit_property(request, propertie_id):
    return HttpResponseNotFound('to be coded.')

def hide_property(request, propertie_id):
    return HttpResponseNotFound('to be coded.')

def unhide_property(request, propertie_id):
    return HttpResponseNotFound('to be coded.')

def bnbuser_details(request, bnbuser_id):
    return HttpResponseNotFound('to be coded.')

