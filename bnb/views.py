from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg, Count

def homepage(request):
    if request.user.is_authenticated():
        recently_added_properties = Propertie.objects.order_by('-creation_date')[:10]
        reservation_requests = Reservation.objects.filter(propertie__owner=request.user).filter(approved=False).order_by('-start_date')
        context = {
            'user': request.user,
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
        if request.user.is_authenticated() and (r.propertie.owner == request.user or request.user.is_superuser):
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
                'show_reservation_form': p.owner != request.user,
                'show_admin_links': request.user.is_superuser or p.owner == request.user,
                'show_submit_review_form': p.owner != request.user,
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
    try:
        if not request.user.is_authenticated():
            #return HttpResponse('okokokok')
            raise PermissionDenied
        p = Propertie.objects.get(pk=propertie_id)
        r = Reservation()
        r.propertie = p
        r.renter = request.user
        r.start_date = request.POST.get('start_date')
        r.end_date = request.POST.get('end_date')
        r.save()

    except ObjectDoesNotExist:
        return HttpResponseNotFound(_('Property not found'))
    except PermissionDenied:
        return HttpResponseForbidden(_('Permission Denied.'))
    except:
        return HttpResponse(_('Unexpected Error:'))
    else:
        return HttpResponse('Reservation Requested.')

def edit_property(request, propertie_id):
    return HttpResponseNotFound('to be coded by Zhengyu, who\'s wondering if there\'s an easier way.')

def hide_property(request, propertie_id):
    # Simplied - Not validating data or handling exceptions.
    try:
        p = Propertie.objects.get(pk=propertie_id)
        p.hidden = True
        p.save()
    except:
        return HttpResponse(_('Unexpected Error:'))
    else:
        return HttpResponse('Property is now hidden. {}'.format(p))

def unhide_property(request, propertie_id):
    # Simplied - Not validating data or handling exceptions.
    try:
        p = Propertie.objects.get(pk=propertie_id)
        p.hidden = False
        p.save()
    except:
        return HttpResponse(_('Unexpected Error:'))
    else:
        return HttpResponse('Property is now not hidden. {}'.format(p))

def review_property(request, propertie_id):
    # Simplied - Not validating data or handling exceptions.
    try:
        r = Review()
        r.reviewer = request.user
        r.propertie = Propertie.objects.get(pk=propertie_id)
        r.rating = request.POST.get('rating')
        r.comment = request.POST.get('comment')
        r.save()
    except:
        return HttpResponse(_('Unexpected Error:'))
    else:
        return HttpResponse('Review Added.')

def user_details(request, bnbuser_id):
    return HttpResponseNotFound('to be coded by Dan.')

