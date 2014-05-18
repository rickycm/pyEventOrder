#coding=utf-8
__author__ = 'Aston'
import time
import logging

import os
from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from models import event as activity


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
            try:
                user = User.objects.get(last_name=openid)
                try:
                    active = activity.objects.filter(updated_by=user.id).latest('updated_date')
                    logger.debug('get activity ' + str(active.id))
                    return sendEvent(fromUser=myid, toUser=openid, active=active)
                except activity.DoesNotExist:
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
    article={'title':title, 'description':'亲，要使用此功能请点击绑定微信！'}
    article['picurl'] = URLBASE + '/media/info.jpg'
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
    #description = u'\<span style=\"color: steelBlue\"\>' + active.event_title + u'\<\/span\> \n' + active.event_date.strftime("%Y-%m-%d %H:%M") + u'\n长按可转发'
    description = active.event_title.encode("utf8") + u'\n' + active.event_date.strftime("%Y-%m-%d %H:%M").encode("utf8") + u'\n长按可转发'
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

