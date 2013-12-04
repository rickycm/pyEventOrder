#coding=utf-8
__author__ = 'Aston'
import time
import logging

from django.http import Http404
from django.shortcuts import render_to_response
from models import wechat_user, event as activity

logger = logging.getLogger('django.dev')
URLBASE = 'http://whitemay.pythonanywhere.com'

def processEvent(msg,event):
    event_type = event.text
    logger.debug('It is a event: ' + event_type)
    if event_type=='subscribe':
        # 这是一个订阅消息。
        # 收到消息后，需要在用户库中做一条记录，并设置为没有设置
            # 考虑在此申请用户信息。
        userid = msg.find('FromUserName').text
        try:
            user = wechat_user.objects.get(openid=userid)
            user.subscribe = True
            user.initialized = False
        except wechat_user.DoesNotExist:
            user = wechat_user.objects.create(openid=userid, subscribe=True, initialized=False)
        user.save()

        return sendSetting(user, msg)

    elif event_type=='CLICK':
        # 目前为止，应该只有SETTING这一个点击项
        click = msg.find('EventKey').text
        if click=='SETTING':
            userid = msg.find('FromUserName').text
            logger.debug(userid + ' clicked!')
            try:
                user = wechat_user.objects.get(openid=userid)
            except wechat_user.DoesNotExist:
                user = wechat_user.objects.create(openid=userid, subscribe=True, initialized=False)
                user.save()
            return sendSetting(user, msg)
        elif click=='GETEVENT':
            myid = msg.find('ToUserName').text
            openid = msg.find('FromUserName').text
            wechatUser = wechat_user.objects.get(openid=openid)
            active = activity.objects.filter(updated_by=wechatUser.id).order_by('-updated_date')[0:1]
            logger.debug('get active ' + active.id)
            return sendEvent(fromUser=myid, toUser=openid, active=active)

    raise Http404

def sendSetting(user, msg):
    # 然后向用户主动发送一条消息，欢迎用户进入设置页面
    # 设置页面的URL中间包括用户的userid
    # 这样用户在打开设置页面时，就可以将userid保存在Cookie中了。
    msg_out={}
    msg_out['toUser'] =  user.openid
    msg_out['fromUser'] = msg.find('ToUserName').text
    logger.debug('My id is ' + msg_out['fromUser'])
    msg_out['time'] = int(time.time())

    if not user.wechat_inputname:
        title = u'您好，陌生人'
    else:
        title = u'您好，'+user.wechat_inputname
    article={'title':title, 'description':'亲，点这里设置您的个人信息，才能正常使用活动功能哦！'}
    article['picurl'] = URLBASE + '/media/badminton.png'
    article['url'] = URLBASE + '/setting/?openid=' + user.openid

    msg_out['articles'] = [article]
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

def sendEvent(fromUser, toUser, active):
    msg_out = {
        'fromUserUser':fromUser,
        'toUser':toUser,
        'time':int(time.time()),
        'article':{
            'title':'活动发布',
            'description':active.event_title,
            'picurl':URLBASE + '/media/badminton.png',
            'url':URLBASE + '/showevent/?' + active.id,
        }
    }
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

