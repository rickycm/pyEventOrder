#coding=utf-8
__author__ = 'Aston'
import time
import logging

import os
from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from models import Event as Activity


logger = logging.getLogger('django.dev')
URLBASE = 'http://'+ os.environ['DJANGO_SITE']

def processEventMessage(msg, event_msg):
    event_type = event_msg.text
    logger.debug('It is a event: ' + event_type)
    if event_type=='subscribe':
        # 这是一个订阅消息。
        # 收到消息后，需要在用户库中做一条记录，并设置为没有设置
            # 考虑在此申请用户信息。
        myid = msg.find('ToUserName').text
        openid = msg.find('FromUserName').text
        # 否则向用户主动发送一条消息，用来绑定用户
        # 设置页面的URL中间包括用户的userid
        msg_out={}
        msg_out['toUser'] = openid
        msg_out['fromUser'] = myid
        msg_out['time'] = int(time.time())

        title = u'您尚未绑定微信'
        article={'title':title, 'description':u'亲，请点击此消息绑定微信。'}
        article['picurl'] = URLBASE + '/media/info.jpg'
        article['url'] = URLBASE + '/checklogin/?openid=' + openid

        msg_out['articles'] = [article]
        #logger.debug(msg_out)
        return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

    elif event_type=='CLICK':
        # 目前为止，应该只有SETTING这一个点击项
        click = msg.find('EventKey').text
        if click=='GETEVENT':
            myid = msg.find('ToUserName').text
            openid = msg.find('FromUserName').text
            try:
                user = User.objects.get(last_name=openid)
                try:
                    active = Activity.objects.filter(updated_by=user.id).latest('updated_date')
                    logger.debug('get activity ' + str(active.id))
                    return sendEvent(fromUser=myid, toUser=openid, active=active)
                except Activity.DoesNotExist:
                    logger.debug('get activity -- activity noexist:')
                    msg_out={
                        'toUser':msg.find('FromUserName').text,
                        'fromUser':msg.find('ToUserName').text,
                        'time':int(time.time()),
                        'content':'您还未发布过活动，请先发布。',
                    }
                    return render_to_response('textmsg.xml', msg_out, content_type='text/xml')
            except User.DoesNotExist:
                # 否则向用户主动发送一条消息，用来绑定用户
                # 设置页面的URL中间包括用户的userid
                msg_out={}
                msg_out['toUser'] = openid
                msg_out['fromUser'] = myid
                msg_out['time'] = int(time.time())

                title = u'您尚未绑定微信'
                article={'title':title, 'description':u'亲，请点击此消息绑定微信。'}
                article['picurl'] = URLBASE + '/media/info.jpg'
                article['url'] = URLBASE + '/checklogin/?openid=' + openid

                msg_out['articles'] = [article]
                #logger.debug(msg_out)
                return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

    raise Http404

def sendEvent(fromUser, toUser, active):
    msg_out = {
        'fromUser':fromUser,
        'toUser':toUser,
        'time':int(time.time()),
    }
    description = '活动：' + active.event_title.encode("utf8") + '\n时间：' + active.event_date.strftime("%Y-%m-%d %H:%M").encode("utf8") + '\n(长按可转发)'
    #description = active.event_title.encode("utf8") + '\n' + active.event_date.strftime("%Y-%m-%d %H:%M").encode("utf8") + '\n长按可转发'
    print description
    article = {
        'title':u'您发布的最新活动',
        'description':description,
        'picurl':URLBASE + '/media/badminton.png',
        'url':URLBASE + '/showevent/?eventid=' + str(active.id),
    }
    msg_out['articles'] = [article]
    #logger.debug(msg_out)
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

