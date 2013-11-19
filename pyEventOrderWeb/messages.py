#coding=utf-8
__author__ = 'Aston'
import time
import logging

from lxml import etree
from django.http import HttpResponse
#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response

logger = logging.getLogger('django.dev')
URLBASE = 'http://whitemay.pythonanywhere.com'


def processEvent(msg,event):
    logger.debug('It is a event.')
    msg_out = etree.Element('XML')
    output_xml = etree.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')

def processMessage(msg):
    logger.debug('It is a message.')

    msg_out={}
    msg_out['toUser'] =  msg.find('FromUserName').text
    msg_out['fromUser'] = msg.find('ToUserName').text
    msg_out['time'] = int(time.time())

    #msg_out['content'] = 'Hello, Ricky!'
    #return render_to_response('textmsg.xml', msg_out, content_type='text/xml')

    article={'title':'发布活动', 'description':'点此链接发布一个活动'}
    article['picurl'] = URLBASE + '/media/test.png'
    article['url'] = URLBASE + '/add_event/?user=' + msg_out['toUser']

    msg_out['articles'] = [article]
    return render_to_response('multimsg.xml', msg_out, content_type='text/xml')

