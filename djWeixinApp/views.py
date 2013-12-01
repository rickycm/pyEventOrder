# coding=utf-8
import logging
import time
import urllib
import json
import urllib2

from django.shortcuts import render_to_response

from forms import SendMessageForm
from models import WeixinApp


logger = logging.getLogger('django.dev')

# Create your views here.
def sendMessage(request):
    if request.method=='GET':
        form = SendMessageForm()
        return render_to_response('jqmform.html',{'title':'title','form':form})
    else:
        form = SendMessageForm(request.POST)
        if form.is_valid():
            sender_id = form.data['sender']
            sender = WeixinApp.objects.get(pk=sender_id)
            now = int(time.time())
            logger.debug(str(now) + ':' + str(sender.expire))

            if now>sender.expire: # token已经过期
                url = 'https://api.weixin.qq.com/cgi-bin/token?' + urllib.urlencode({
                    'grant_type':'client_credential',
                    'appid':sender.app_id,
                    'secret':sender.app_secret,
                })
                logger.debug(url)
                f = urllib.urlopen(url)
                jobj = json.load(f)
                f.close()
                logger.debug('Thread return 1: ' + str(jobj))
                if jobj.has_key('errmsg'):
                    logger.error('WX get error: ' + jobj['errmsg'])
                    return render_to_response('errorMessage.html',{'errorMessage':jobj['errmsg']})
                else:
                    access_token = jobj['access_token']
                    sender.expire = now + jobj['expires_in']
                    sender.access_token = access_token
                    sender.save()
            else:
                access_token = sender.access_token

            logger.debug('access_token is ' + access_token)
            receiver = form.data['receiver']
            message = form.data['message']
            msg = {'touser':receiver,'msgtype':'text','text':{'content':message}}
            #logger.debug(json.dumps(msg))

            url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?" + urllib.urlencode({
                'access_token':access_token,
            })
            req = urllib2.Request(url, json.dumps(msg), {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            jobj = json.load(f)
            f.close()
            logger.debug('Thread return 2: ' + str(jobj))
            if jobj.has_key('errmsg'):
                logger.error('WX get error: ' + jobj['errmsg'])
                return render_to_response('errorMessage.html',{'errorMessage':jobj['errmsg']})
            else:
                return render_to_response('errorMessage.html',{'errorMessage':'发送成功'})
        else:
            return render_to_response('jqmform.html',{'title':'title','form':form})