#coding=utf-8
__author__ = 'Aston'
import time
import logging
import os

from django.shortcuts import render_to_response

logger = logging.getLogger('django.dev')
URLBASE = 'http://' + os.environ['DJANGO_SITE']

def processMessage(msg):
    logger.debug('It is a message.')

    m_type = msg.find('MsgType').text
    if m_type=='text':
        return processText(msg)

    msg_out={}
    msg_out['toUser'] =  msg.find('FromUserName').text
    msg_out['fromUser'] = msg.find('ToUserName').text
    msg_out['time'] = int(time.time())

    article={'title':'发布活动', 'description':'点此链接发布一个活动'}
    article['picurl'] = URLBASE + '/media/test.png'
    article['url'] = URLBASE + '/add_event/'

    msg_out['articles'] = [article]
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

def processText(msg):
    m_content = msg.find('Content').text.lower()
    msg_out={
        'toUser':msg.find('FromUserName').text,
        'fromUser':msg.find('ToUserName').text,
        'time':int(time.time()),
    }
    if m_content=='menu':
        msg_out['content'] = '选择你想要进行的操作：\n\n' \
            + '<a href="' + URLBASE+ '/add_event/' + '">*发布活动;</a> \n\n' \
            + '<a href="' + URLBASE+ '/list_events/?type=mine' + '">*查询我发布的活动；</a>\n\n' \
            + '<a href="' + URLBASE+ '/list_events/?type=other' + '">*查询我参与的活动。</a>'
    elif m_content=='set':
        msg_out['content'] = '亲，请<a href="' + URLBASE + '/setting/?openid=' + msg_out['toUser'] + '">戳这里设置您的名字</a>，才能正常使用活动功能哦！'
    else:
        msg_out['content'] = '您的消息将被记录下来，并在适当的时候回复您。谢谢！'
    return render_to_response('textmsg.xml', msg_out, content_type='text/xml')
