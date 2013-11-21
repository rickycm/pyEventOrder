#coding=utf-8
import logging
import datetime

from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from pyEventOrderWeb import forms
from pyEventOrderWeb.models import *

logger = logging.getLogger('django.dev')

def login_form(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            form = forms.LoginForm(request.POST)
            login(request, user)
            # Redirect to a success page.
            return render_to_response("index.html", {'user': user})
            #return HttpResponseRedirect("/")
        else:
            form = forms.LoginForm()
            # Return an error message.
            return render_to_response("login.html", {'msg': "请重新输入账户", 'form': form}, context_instance=RequestContext(request))
    except:
        form = forms.LoginForm()
        return render_to_response("login.html", {'msg': "请重新登录", 'form': form}, context_instance=RequestContext(request))


def register(request):
        form = UserCreationForm()
        if request.method == 'GET':
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        return HttpResponseRedirect("/")

def index(request):
    #if request.user.is_authenticated():
        user = request.user
        return render_to_response("index.html", {'user': user}, context_instance=RequestContext(request))
    #return HttpResponseRedirect("/accounts/login/")

def list_events(rq):
        ONE_PAGE_OF_DATA = 10
        if rq.user.is_authenticated():
            user = rq.user
            if user.is_superuser == 1:
                try:
                    curPage = int(rq.GET.get('curPage', '1'))
                    allPage = int(rq.GET.get('allPage','1'))
                    pageType = str(rq.GET.get('pageType', ''))
                except ValueError:
                    curPage = 1
                    allPage = 1
                    pageType = ''

                #判断点击了【下一页】还是【上一页】
                if pageType == 'pageDown':
                    curPage += 1
                elif pageType == 'pageUp':
                    curPage -= 1

                startPos = (curPage - 1) * ONE_PAGE_OF_DATA
                endPos = startPos + ONE_PAGE_OF_DATA
                events = event.objects.all()[startPos:endPos]

                if curPage == 1 and allPage == 1: #标记1
                    allPostCounts = event.objects.count()
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1

                return render_to_response("list_event.html", {'user': user, 'events':events, 'allPage':allPage, 'curPage':curPage}, context_instance=RequestContext(rq))
            else:
                user = rq.user
                try:
                    curPage = int(rq.GET.get('curPage', '1'))
                    allPage = int(rq.GET.get('allPage','1'))
                    pageType = str(rq.GET.get('pageType', ''))
                except ValueError:
                    curPage = 1
                    allPage = 1
                    pageType = ''

                #判断点击了【下一页】还是【上一页】
                if pageType == 'pageDown':
                    curPage += 1
                elif pageType == 'pageUp':
                    curPage -= 1

                startPos = (curPage - 1) * ONE_PAGE_OF_DATA
                endPos = startPos + ONE_PAGE_OF_DATA
                events = event.objects.filter(updated_by=user)[startPos:endPos]

                if curPage == 1 and allPage == 1:  #标记1
                    allPostCounts = event.objects.count()
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1

                return render_to_response("list_event.html", {'user': user, 'events':events, 'allPage':allPage, 'curPage':curPage}, context_instance=RequestContext(rq))
        return HttpResponseRedirect("/accounts/login/")

# 添加一个活动
@login_required
def add_event(request):
    if request.method == 'GET':
        form = forms.EventForm()
        return render_to_response('addEvent.html', {'title': '新建活动', 'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = forms.EventForm(request.POST)
        if form.is_valid():
            username = request.user.username
            e = event.objects.create(
                updated_by = form.cleaned_data['updated_by'],
                event_title = form.cleaned_data['event_title'],
                event_detail = form.cleaned_data['event_detail'],
                event_date = form.cleaned_data['event_date'],
                event_limit = form.cleaned_data['event_limit'],
                updated_date = datetime.datetime.now(),
            )
            e.save()
            return list_events(request)
        else:
            return render_to_response('addEvent.html', {'title': '新建活动', 'form': form},
                                  context_instance=RequestContext(request))

# 添加一个活动
@login_required
def add_event2(request):
    if request.method == 'GET':
        form = forms.EventForm2()
        return render_to_response('addEvent2.html', {'title': '新建活动', 'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = forms.EventForm2(request.POST)
        s = datetime.datetime.strptime(form.data['eventdate'] + ' ' + form.data['eventtime'], "%Y-%m-%d %H:%M")
        if form.is_valid():
            e = event.objects.create(
                event_title = form.data['event_title'],
                event_detail = form.data['event_detail'],
                event_date = s,
                event_limit = form.data['event_limit'],
                updated_by = "11111111111",
                event_type = 1,
            )
            e.save()
            return list_events(request)
        else:
            return render_to_response('addEvent2.html', {'title': '新建活动', 'form': form}, context_instance=RequestContext(request))

# 处理消息机制，应该是公众平台中最核心的处理部分
import hashlib
from lxml import etree
from messages import processMessage
from events import processEvent

def message(request):
    # 对于任何消息，都需要通过下面的代码来确认消息的合法性。
    # 这里的假定是，即使在POST模式下，依然可以通过GET方式来获得参数。
    # 以下代码需要在实际工作环境中检验其正确性
    logger.debug('get a message: ')
    try:
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        token = 'WeiXin'

        tmpArr = sorted([token, timestamp, nonce])
        tmpStr = ''.join(tmpArr)
        tmpStr = hashlib.sha1(tmpStr).hexdigest()

        # 当两者相等时，消息合法。
        if tmpStr == signature:
            if request.method == 'GET':
                # GET消息表示仅仅是对公众账号后台进行校验。
                echostr = request.GET['echostr']
                return HttpResponse(echostr)
            elif request.method == 'POST':
                # 这种方式下应该是实际的消息数据
                # 消息可分为两种：用户发过来的消息，系统事件。
                # 使用函数来进行进一步处理。
                #logger.debug(request.body)
                msg_in = etree.parse(request)
                event = msg_in.find('Event')
                if event==None : #这是一个事件
                    return processMessage(msg_in)
                else: #这是一个消息
                    return processEvent(msg_in,event)
        else:
            logger.info('Illedge message received')
            raise Http404
    except Exception as e: # 此处仅保留，实际情况是无需进行任何处理。
        logger.info('Exception received: ' + e.message)
        raise e

#APP ID：100561618
#APP KEY：dbbea5729ffd5182deff63f90131bc3b
from django.http import Http404
from urllib import urlencode
def setting(request):
    if not request.user.is_authenticated():
        url = request.build_absolute_uri()
        logger.debug(url)
        request.session['url'] = url
        auth_url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode({'response_type':'code',
            'client_id':'100561618',
            'redirect_url':'http://whitemay.pythonanywhere.com/oauth/'})
        logger.debug(auth_url)
        return HttpResponseRedirect(auth_url)
    if request.method=='GET':
        if request.GET.has_key('userid'):
            userid = request.GET['userid']
            logger.debug('Request has userid ' + userid)
            max_age = 365 * 24 * 60 * 60
            path = request.path
            logger.debug('Path is ' + path)
            response = HttpResponseRedirect(path)
            response.set_cookie("wxopenid", userid, max_age=max_age)
            return response

        if request.COOKIES.has_key('wxopenid'):
            userid = request.COOKIES['wxopenid']
            logger.info('Cookie has userid ' + userid)
        else:
            raise Http404

        user = wechat_user.objects.get(openid=userid)
        form = forms.SettingForm({'inputname':user.wechat_inputname,'data_id':user.id,})
        return render_to_response('addEvent.html', {'title': '个人设置', 'form': form},
            context_instance=RequestContext(request))
    else: #POST
        if request.COOKIES.has_key('wxopenid'):
            userid = request.COOKIES['wxopenid']
            logger.info('Cookie has userid ' + userid)
        else:
            raise Http404

        form = forms.SettingForm(request.POST)
        if form.is_valid():
            user = wechat_user.objects.get(id=form.cleaned_data['data_id'])
            assert user.openid==userid
            user.wechat_inputname = form.cleaned_data['inputname']
            user.save()
            return list_events(request)
        else:
            return render_to_response('addEvent.html', {'title': '个人设置', 'form': form},
                context_instance=RequestContext(request))
