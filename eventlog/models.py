from django.db import models

# Create your models here.
class Events(models.Model):
  event = models.CharField(max_length=255, null=False)

  def __str__(self):
    return "{}".format(self.event);