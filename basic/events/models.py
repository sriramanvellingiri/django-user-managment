from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Events(models.Model):
    TYPE = (
                ('PARTY','PARTY'),
                ('MARRIAGE','MARRIAGE'),
                ('BIRTHDAY','BIRTHDAY'),
            );
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20,choices=TYPE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    participants = models.ManyToManyField(User,related_name="EventParticipants")
    city = models.CharField(max_length=255,null = True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="createdby")
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type+' '+self.city

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    data = JSONField()


class FileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    file_data = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=False, null=False)

    def __str__(self):
        return self.file_data.name

