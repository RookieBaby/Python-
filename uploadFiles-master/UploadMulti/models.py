from __future__ import unicode_literals

from django.db import models

class Photo(models.Model):
    codes = models.CharField(max_length=255, blank=True)
    filename = models.CharField(max_length=255, blank=True)
    photos = models.FileField(upload_to='photos/')
    videos = models.FileField(upload_to='video/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
# class Types(models.Model):
#     types = models.CharField(max_length=255)
#     codes = models.CharField(max_length=255)
    class Meta:
        db_table = "tbl_LiveSchool"  # 更改表名
class Types(models.Model):
    ChannelID = models.CharField(max_length=36,primary_key=True)
    ChannelName = models.CharField(max_length=50)
    ChannelCode = models.CharField(max_length=200)
    class Meta:
        db_table = "tbl_LiveChannel"  # 更改表名