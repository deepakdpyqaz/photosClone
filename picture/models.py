from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Picture(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    picture = models.FileField(upload_to="picture")
    uploaded_at = models.DateTimeField(default=timezone.now())