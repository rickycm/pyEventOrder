#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
EVENT_TYPE = [(1, u'体育活动'), (2, u'聚餐聚会'), (0, u'推广活动')]
PARTICI_TYPE = [(0, u'不参加'), (1, u'参加'), (2, u'可能参加'), (5, u'未报名'), (10, u'活动发起人')]
EVENT_STATUS = [(0, u'可报名'), (1, u'报名人满'), (2, u'已取消'), (3, u'已停止报名'), (4, u'已过期')]

class Event(models.Model):
    event_title = models.CharField(max_length=200)
    event_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    event_detail = models.TextField(max_length=100000)
    updated_by = models.ForeignKey(User)
    event_type = models.IntegerField(blank=True, choices=EVENT_TYPE, default=1)
    event_registdeadline = models.DateTimeField(blank=True, null=True)
    event_hostname = models.CharField(max_length=20, blank=True)
    event_limit = models.IntegerField(default=0, blank=True)
    event_sn = models.CharField(max_length=20, blank=True)  # 保存推广活动邀请码等
    event_status = models.IntegerField(default=0, choices=EVENT_STATUS, blank=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ["-updated_date"]
    def __unicode__(self):
        return u'%s' % (self.event_title)

class Participant(models.Model):
    event_ID = models.ForeignKey(Event)
    # 如果没有弄错，下面这个字段应该也是多余的。
    event_sn = models.CharField(max_length=200, blank=True)
    partici_name = models.CharField(max_length=20)
    partici_type = models.IntegerField(choices=PARTICI_TYPE, default=5)
    register_time = models.DateTimeField(auto_now=True)

    partici_user = models.ForeignKey(User)
    partici_openid = models.CharField(max_length=30, blank=True)
    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ["event_ID", "partici_type", "register_time"]
        unique_together = (('event_ID', 'partici_user'),)
    def __unicode__(self):
        return u'%s' % (self.partici_name)
