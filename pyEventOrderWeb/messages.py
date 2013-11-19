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
    msg_out['content'] = 'Hello, Ricky!'

    #t = get_template('textmsg.xml')
    #output_xml = t.render(Context(msg_out))
    #logger.debug('Output is ' + output_xml)

    #msg_out = etree.Element('XML')
    #output_xml = etree.tostring(msg_out)
    #logger.debug(output_xml)
    return render_to_response('textmsg.xml', msg_out, content_type='text/xml')
    #return HttpResponse(output_xml, content_type='text/xml')

