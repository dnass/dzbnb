from django.db import models
from django.conf import settings #To reference the User model, see https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#referencing-the-user-model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class Property(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

class View(models.Model):
	property = models.ForeignKey(Property, on_delete=models.CASCADE)
	viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	view_time = models.DateTimeField(auto_now_add=True) #https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.DateTimeField
