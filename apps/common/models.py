from django.db import models
from apps.common.utils import upload


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Banner(BaseModel):
    image = models.ImageField(upload_to=upload, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title