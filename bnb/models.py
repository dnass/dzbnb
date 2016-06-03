from django.db import models
from django.conf import settings #To reference the User model, see https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#referencing-the-user-model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

class BNBUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    reg_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    login_count = models.IntegerField(default=0)

	def __str__(self):
		u = User.objects.get(id=self.user)
		return '{}. {}'.format(self.id, u.username)

	def clean(self):
		errors = {}
		if self.last_login < self.reg_time:
			errors['last_login'] = ValidationError(_('Last login time must be greater than or equal to registration time.'))
		if self.login_count < 0:
			errors['login_count'] = ValidationError(_('Login count must be greater than or equal to 0.'))
		if errors:
			raise ValidationError(errors)

class Property(models.Model):
	owner = models.ForeignKey(BNBUser, on_delete=models.CASCADE)
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

	class Meta: #https://docs.djangoproject.com/en/1.9/topics/db/models/#meta-options
		get_latest_by = ["creation_date"]
		verbose_name_plural = "properties"

	def __str__(self):
		return '{}. {}'.format(self.id, self.name)

class Reservation(models.Model):
	property = models.ForeignKey(Property, on_delete=models.CASCADE)
	renter = models.ForeignKey(BNBUser, on_delete=models.CASCADE)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	approved = models.BooleanField(default=False)

	def clean(self):
		if start_date > end_date:
			raise ValidationError({'date': _('Start date cannot be later than end date.')})

class Review(models.Model):
	reviewer = models.ForeignKey(BNBUser, on_delete=models.CASCADE)
	property = models.Foreignkey(Property, on_delete=models.CASCADE)
	hidden = models.BooleanField(default=False)
	rating = models.IntegerField()
	comment = models.TextField(max_length=4096)
	review_time = models.DateTimeField(auto_now_add=True)

	def clean(self):
		if rating < 1 or rating > 5:
			raise ValidationError({'rating': _('Rating must be integer between 1 and 5.')})

class View(models.Model):
	property = models.ForeignKey(Property, on_delete=models.CASCADE)
	viewer = models.ForeignKey(BNBUser, on_delete=models.CASCADE)
	view_time = models.DateTimeField(auto_now_add=True) #https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.DateTimeField
