#coding=utf-8
__author__ = 'Aston'
import time
import logging
import os

from django.http import Http404
from django.shortcuts import render_to_response
from models import wechat_user, event as activity
from django.contrib.auth.models import User

logger = logging.getLogger('django.dev')
URLBASE = 'http://'+ os.environ['DJANGO_SITE']

def processEventMessage(msg, event_msg):
    event_type = event_msg.text
    logger.debug('It is a event: ' + event_type)
    if event_type=='subscribe':
        # 这是一个订阅消息。
        # 收到消息后，需要在用户库中做一条记录，并设置为没有设置
            # 考虑在此申请用户信息。
        userid = msg.find('FromUserName').text
        try:
            user = User.objects.get(last_name=userid)
            #user.subscribe = True
            #user.save()
        except User.DoesNotExist:
            user = None
        return sendSetting(user, msg)

    elif event_type=='CLICK':
        # 目前为止，应该只有SETTING这一个点击项
        click = msg.find('EventKey').text
        if click=='SETTING':
            userid = msg.find('FromUserName').text
            logger.debug(userid + ' clicked!')
            try:
                user = User.objects.get(last_name=userid)
            except User.DoesNotExist:
                user = None
            return sendSetting(user, msg)
        elif click=='GETEVENT':
            myid = msg.find('ToUserName').text
            openid = msg.find('FromUserName').text
            user = User.objects.get(last_name=openid)
            active = activity.objects.filter(updated_by=user.id).latest('updated_date')
            logger.debug('get activity ' + str(active.id))
            return sendEvent(fromUser=myid, toUser=openid, active=active)

    raise Http404

def sendSetting(user, msg):
    # 然后向用户主动发送一条消息，欢迎用户进入设置页面
    # 设置页面的URL中间包括用户的userid
    # 这样用户在打开设置页面时，就可以将userid保存在Cookie中了。
    msg_out={}
    msg_out['toUser'] =  msg.find('FromUserName').text
    msg_out['fromUser'] = msg.find('ToUserName').text
    logger.debug('My id is ' + msg_out['fromUser'])
    msg_out['time'] = int(time.time())

    if (user is None) or (not user.first_name):
        title = u'您好，陌生人'
    else:
        title = u'您好，'+user.first_name
    article={'title':title, 'description':'亲，为了更好地使用活动功能，请点这里设置您的信息！'}
    article['picurl'] = URLBASE + '/media/info.png'
    article['url'] = URLBASE + '/setting/?openid=' + user.last_name

    msg_out['articles'] = [article]
    #logger.debug(msg_out)
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

def sendEvent(fromUser, toUser, active):
    msg_out = {
        'fromUser':fromUser,
        'toUser':toUser,
        'time':int(time.time()),
    }
    article = {
        'title':u'活动发布',
        'description':active.event_title,
        'picurl':URLBASE + '/media/badminton.png',
        'url':URLBASE + '/showevent/?eventid=' + str(active.id),
    }
    msg_out['articles'] = [article]
    #logger.debug(msg_out)
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

