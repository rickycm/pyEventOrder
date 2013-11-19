#coding=utf-8
__author__ = 'Aston'
from lxml import etree
import logging
logger = logging.getLogger('django.dev')

from django.http import HttpResponse

def processEvent(msg,event):
    logger.debug('It is a event.')
    msg_out = etree.Element('XML')
    output_xml = ET.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')

def processMessage(msg):
    logger.debug('It is a message.')
    sender = msg.find('FromUserName').text
    logger.debug('Sender is ' + sender)
    msg_out = etree.Element('XML')
    output_xml = etree.tostring(msg_out)
    logger.debug(output_xml)
    return HttpResponse(output_xml, content_type='text/xml')
