#coding=utf-8
from django.db import models

# Create your models here.
EVENT_TYPE = [(1, 'event'), (2, 'order')]
PARTICI_TYPE = [(0, u'不参加'), (1, u'参加'), (2, u'可能参加'), (5, u'未报名'), (10, u'活动发起人')]
EVENT_STATUS = [(0, u'可报名'), (1, u'报名人满'), (2, u'已取消'), (3, u'已停止报名')]

class event(models.Model):
    event_title = models.CharField(max_length=200)
    event_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    event_detail = models.TextField(max_length=100000)
    updated_by = models.CharField(max_length=100, blank=True, null=True) # wechat_user.id
    event_type = models.IntegerField(blank=True, choices=EVENT_TYPE, default=1)
    event_registdeadline = models.DateTimeField(blank=True, null=True)
    event_hostfakeID = models.CharField(max_length=200)
    event_hostname = models.CharField(max_length=1000, blank=True)
    event_limit = models.IntegerField(default=0, blank=True)
    event_sn = models.CharField(max_length=20, blank=True)
    event_status = models.IntegerField(default=0, choices=EVENT_STATUS, blank=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ["-updated_date"]
    def __unicode__(self):
        return u'%s' % (self.event_title)


class wechat_user(models.Model):
    wechat_fakeID = models.CharField(max_length=200, blank=True, null=True)
    wechat_username = models.CharField(max_length=200, blank=True, null=True)
    wechat_inputname = models.CharField(max_length=200, blank=True, null=True)
    wechat_usertype = models.CharField(max_length=20, blank=True, null=True)

    subscribe = models.BooleanField()
    openid = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    sex = models.NullBooleanField(default=None)
    language = models.CharField(max_length=10, default='zh-CN', blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, default='中国', blank=True, null=True)
    headimageurl = models.URLField(max_length=200, blank=True, null=True)

    # 本字段表明用户保存了Cookie，设置了用户名，从而可以完成系统内的主要工作。
    initialized = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = 'WechatUser'
        verbose_name_plural = 'WechatUsers'

    def __unicode__(self):
        return u'%s' % (self.wechat_username)

class participant(models.Model):
    partici_fakeID = models.CharField(max_length=200)
    event_ID = models.ForeignKey(event)
    event_sn = models.CharField(max_length=200, blank=True)
    partici_name = models.CharField(max_length=200)
    partici_type = models.IntegerField(choices=PARTICI_TYPE, default=5)
    register_time = models.DateTimeField(auto_now_add=True)

    partici_user = models.ForeignKey(wechat_user)
    partici_openid = models.CharField(max_length=30, blank=True)
    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ["event_ID", "partici_type", "register_time"]
        unique_together = (('event_ID', 'partici_user'),)
    def __unicode__(self):
        return u'%s' % (self.partici_name)
