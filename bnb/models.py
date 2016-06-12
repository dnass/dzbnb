from django.db import models
from django.conf import settings #To reference the User model, see https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#referencing-the-user-model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

BLACK_STAR = u"\u2605"
WHITE_STAR = u"\u2606"

class BNBUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    login_count = models.IntegerField(default=0)
    # Fields from User (Table: auth_user)
        # username : varchar(30)
        # email : varchar(254)
        # password : varchar(128)
        # is_staff : bool
        # is_active : bool
        # is_superuser : bool
        # date_joined : datetime
        # last_login : datetime

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.login_count < 0:
            raise ValidationError({'login_count': _('Login count must be greater than or equal to 0.')})

class Propertie(models.Model): # altered spelling to avoid Python's reserved word property.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    hidden = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    size = models.FloatField()
    price = models.FloatField()
    description = models.CharField(max_length=4096)

    def clean(self): #https://docs.djangoproject.com/en/1.9/ref/models/instances/#validating-objects
        errors = {}
        if self.size <= 0:
            errors['size'] = ValidationError(_('Size must be bigger than 0.'))
        if self.price < 0:
            errors['price'] = ValidationError(_('Price must be higher or equal to 0.'))
        if errors:
            raise ValidationError(errors)
        # NEED FIX: empty entry in form causes TypeError: unorderable types: NoneType() <= int()

    class Meta: #https://docs.djangoproject.com/en/1.9/topics/db/models/#meta-options
        get_latest_by = ["creation_date"]
        verbose_name = "property"
        verbose_name_plural = "properties"

    def __str__(self):
        return '{}. {}'.format(self.id, self.name)

class Reservation(models.Model):
    propertie = models.ForeignKey(Propertie, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '{}. {}\'s property requested by {}'.format(self.id, self.propertie.owner.user, self.renter.user)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_('End date must be later than Start Date.'))

@python_2_unicode_compatible
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    propertie = models.ForeignKey(Propertie, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    rating = models.IntegerField()
    comment = models.TextField(max_length=4096)
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}{} {}'.format(BLACK_STAR*self.rating, WHITE_STAR*(5-self.rating), self.propertie.name)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': _('Rating must be integer between 1 and 5.')})
        # NEED FIX: empty entry in form causes TypeError: unorderable types: NoneType() <= int()

class View(models.Model):
    propertie = models.ForeignKey(Propertie, on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True) #https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.DateTimeField
