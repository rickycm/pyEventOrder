#coding=utf-8
__author__ = 'Aston'
import time
import logging

#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response

logger = logging.getLogger('django.dev')
URLBASE = 'http://www.eztogether.net'

def processMessage(msg):
    logger.debug('It is a message.')

    m_type = msg.find('MsgType').text
    if m_type=='text':
        return processText(msg)

    msg_out={}
    msg_out['toUser'] =  msg.find('FromUserName').text
    msg_out['fromUser'] = msg.find('ToUserName').text
    msg_out['time'] = int(time.time())

    #msg_out['content'] = 'Hello, Ricky!'
    #return render_to_response('textmsg.xml', msg_out, content_type='text/xml')

    article={'title':'发布活动', 'description':'点此链接发布一个活动'}
    article['picurl'] = URLBASE + '/media/test.png'
    article['url'] = URLBASE + '/add_event/'

    msg_out['articles'] = [article]
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

def processText(msg):
    m_content = msg.find('Content').text
    msg_out={
        'toUser':msg.find('FromUserName').text,
        'fromUser':msg.find('ToUserName').text,
        'time':int(time.time()),
    }
    if m_content=='menu':
        msg_out['content'] = '选择你想要进行的操作：\n\n' \
            + '<a href="">*发布活动;</a> \n\n' \
            + '<a href="">*查询我发布的活动；</a>\n\n' \
            + '<a href="">*查询我参与的活动。</a>'
    elif m_content=='set':

        #article={'title':'信息设置', 'description':'点这里设置您的信息'}
        #article['picurl'] = URLBASE + '/media/test.png'
        #article['url'] = URLBASE + '/setting/?userid=' + msg_out['toUser']

        #msg_out['articles'] = [article]
        #return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

        msg_out['content'] = '<a href="' + URLBASE + '/setting/?openid=' + msg_out['toUser'] + '">点这里设置您的信息</a>'
    return render_to_response('textmsg.xml', msg_out, content_type='text/xml')
