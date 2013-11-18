#coding=utf-8
__author__ = 'Aston'
import xml.etree.ElementTree as ET

from django.http import HttpResponse


def processEvent(msg,event):
    msg_out = ET.Element('XML')
    output_xml = ET.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')

def processMessage(msg):
    msg_out = ET.Element('XML')
    output_xml = ET.tostring(msg_out)
    return HttpResponse(output_xml, content_type='text/xml')
