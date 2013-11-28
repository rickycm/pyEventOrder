#coding=utf-8
__author__ = 'Aston'
import time
import logging

from django.http import Http404
from django.shortcuts import render_to_response
from models import wechat_user

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

        return sendSetting(userid, msg)

    elif event_type=='CLICK':
        # 目前为止，应该只有SETTING这一个点击项
        assert msg.find('EventKey').text == 'SETTING'
        userid = msg.find('FromUserName').text
        logger.debug(userid + 'clicked!')
        try:
            wechat_user.objects.get(openid=userid)
        except wechat_user.DoesNotExist:
            user = wechat_user.objects.create(openid=userid, subscribe=True, initialized=False)
            user.save()
        return sendSetting(userid, msg)

    raise Http404

def sendSetting(userid, msg):
    # 然后向用户主动发送一条消息，欢迎用户进入设置页面
    # 设置页面的URL中间包括用户的userid
    # 这样用户在打开设置页面时，就可以将userid保存在Cookie中了。
    msg_out={}
    msg_out['toUser'] =  userid
    msg_out['fromUser'] = msg.find('ToUserName').text
    logger.debug('My id is ' + msg_out['fromUser'])
    msg_out['time'] = int(time.time())

    article={'title':'欢迎', 'description':'使用之前，请点这里设置您的个人信息。'}
    article['picurl'] = URLBASE + '/media/badminton.png'
    article['url'] = URLBASE + '/setting/?openid=' + userid

    msg_out['articles'] = [article]
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')
