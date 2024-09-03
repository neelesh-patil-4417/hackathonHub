import uuid
from django.db import models

# Create your models here.
class Hackathon(models.Model):
  hack_id = f"hack_{models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)}"
  tittle = models.CharField(max_length=100, blank=False)
  description = models.TextField(max_length=1000, default=None)
  background_image = models.ImageField(upload_to='hackathon_images', blank=True, null=True)