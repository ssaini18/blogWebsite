from django.db import models
from django.contrib.auth.models import User, Permission

# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, default=1)
	title = models.CharField(max_length=100)
	body = models.TextField()
	date = models.DateTimeField()


	def __str__(self):
		return self.title
