from typing import Any
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



# Create your models here.
class Hackathon(models.Model):

  hack_id = models.CharField(max_length=100, primary_key=True)
  tittle = models.CharField(max_length=100, blank=False)
  description = models.TextField(max_length=1000, default=None)
  background_image = models.ImageField(upload_to='background_images',blank=True, null=True)
  hackathon_image = models.ImageField(upload_to='hackathon_images',blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  started_at = models.DateTimeField()
  ended_at = models.DateTimeField()
  reward_price = models.CharField(max_length = 100, default = 10)
  is_active = models.BooleanField(default=False)

  HACKATHON_SUBMISSION_CHOICES = [
        ("file", 'File'),
        ("image", 'Image'),
        ("link", 'Link'),
    ]

  hackathon_submission_type = models.CharField(max_length=10, choices=HACKATHON_SUBMISSION_CHOICES ,default="Link") #because multiple users can participate in multiple hackathon and vice-versa
  user = models.ManyToManyField(User,related_name="hackathons")

  def __str__(self) -> str:
    print(self.hack_id)
    return str(self.tittle) + " created_at " + str(self.created_at)
  
  def save(self, *args, **kwargs) -> Any:
      if not self.hack_id:  # Set hack_id only if it's not already set
          self.hack_id = "hack_" + str(uuid.uuid4())
      super().save(*args, **kwargs)
     
  


class Submission(models.Model):
  submission_id = models.CharField(max_length=100, primary_key=True)
  description = models.TextField(blank = False)  #Keeping description mandatory 
 
  USER_SUBMISSION_CHOICES = [
        ("file", 'File'),
        ("image", 'Image'),
        ("link", 'Link'),
    ]

  user_submission_type = models.CharField(max_length=10, choices=USER_SUBMISSION_CHOICES, default="Link")
  user_submission = models.TextField(max_length=50)

  hackathon =models.ForeignKey(Hackathon,on_delete=models.CASCADE, related_name="submissions") #there can be multiple submissions to one hackathon
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="submissions")


  # class Meta:
  #       constraints = [
  #           models.UniqueConstraint(fields=['user', 'hackathon'], name='unique_user_hackathon_submission')
  #       ]
  # by using above constraint we can make one user to submit only one submission of each hackathon

  def save(self, *args, **kwargs):
      if self.hackathon.hackathon_submission_type != self.user_submission_type:
          raise ValidationError(f"Submission type must match the hackathon's submission type '{self.hackathon.hackathon_submission_type}'.")
      if not self.submission_id:  # Set submission_id only if it's not already set
          self.submission_id = "sub_" + str(uuid.uuid4())
      super().save(*args, **kwargs)


  def __str__(self) -> str:
    return str(self.submission_id)