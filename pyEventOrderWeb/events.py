#coding=utf-8
__author__ = 'Aston'
import time
import logging

from lxml import etree
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import wechat_user

logger = logging.getLogger('django.dev')
URLBASE = 'http://whitemay.pythonanywhere.com'

def processEvent(msg,event):
    logger.debug('It is a event.')
    if event.text=='subscribe':
        # 这是一个订阅消息。
        userid = msg.find('FromUserName').text
        try:
            user = wechat_user.objects.get(openid=userid)
            user.subscribe = True
            user.initialized = False
        except wechat_user.DoseNotExist:
            user = wechat_user.objects.create(openid=userid, subscribe=True, initialized=False)
        user.save()

        # 收到消息后，需要在用户库中做一条记录，并设置为没有设置
            # 考虑在此次申请用户信息。
        # 然后向用户主动发送一条消息，欢迎用户进入设置页面
        # 设置页面的URL中间包括用户的userid
        # 这样用户在打开设置页面时，就可以将userid保存在Cookie中了。
        msg_out={}
        msg_out['toUser'] =  userid
        msg_out['fromUser'] = msg.find('ToUserName').text
        msg_out['time'] = int(time.time())

        article={'title':'欢迎', 'description':'请点这里设置您的其它信息。'}
        article['picurl'] = URLBASE + '/media/test.png'
        article['url'] = URLBASE + '/setting/?userid=' + userid

        msg_out['articles'] = [article]
        return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

    msg_out = etree.Element('XML')
    output_xml = etree.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')

