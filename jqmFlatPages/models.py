from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class JqmFlatPage(models.Model):
    title = models.CharField(max_length=20,blank=True)
    page_id = models.CharField(max_length=50,blank=False,unique=True)
    page_content = HTMLField()

    class Meta:
        db_table = 'jqm_flat_pages'
