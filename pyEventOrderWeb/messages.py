#coding=utf-8
__author__ = 'Aston'
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger('django.dev')

from django.http import HttpResponse

def processEvent(msg,event):
    logger.debug('It is a event.')
    msg_out = ET.Element('XML')
    output_xml = ET.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')

def processMessage(msg):
    logger.debug('It is a message.')
    msg_out = ET.Element('XML')
    output_xml = ET.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')
