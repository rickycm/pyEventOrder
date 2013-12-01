#coding=utf-8
from django.db import models

# 用于保存微信账号有关的信息，可能存在多个微信账号
class WeixinApp(models.Model):
    openid = models.CharField(max_length=30, primary_key=True)
    information = models.TextField('说明信息')
    app_id = models.CharField(max_length=20, blank=True)
    app_secret = models.CharField(max_length=32, blank=True)
    access_token = models.CharField(max_length=150, blank=True)
    expire = models.IntegerField(default=0)
    def __unicode__(self):
        return self.information
    class Meta:
        db_table = 'mp_weixin'