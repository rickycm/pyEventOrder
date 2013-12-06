#coding=utf-8
import logging
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from pyEventOrderWeb import forms
from pyEventOrderWeb.models import *

logger = logging.getLogger('django.dev')

@csrf_protect
def login_form(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            form = forms.LoginForm(request.POST)
            request.session["userid"] = user.id
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


@csrf_protect
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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


#活动列表
@login_required
@csrf_protect
def list_events(rq):
    try:
        userId = rq.session["userid"]
        wechatUser = wechat_user.objects.get(pk=userId)
    except:
        return HttpResponseRedirect('/welcome/')
    events =[]
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

            return render_to_response("list_event.html", {'title': '活动列表', 'user': user, 'events':events, 'allPage':allPage, 'curPage':curPage}, context_instance=RequestContext(rq))
        else:
            user = rq.user
            try:
                curPage = int(rq.GET.get('curPage', '1'))
                allPage = int(rq.GET.get('allPage','1'))
                pageType = str(rq.GET.get('pageType', ''))
                type = str(rq.GET.get('type', 'mine'))
            except ValueError:
                curPage = 1
                allPage = 1
                pageType = ''
                type = 'mine'

            #判断点击了【下一页】还是【上一页】
            if pageType == 'pageDown':
                curPage += 1
            elif pageType == 'pageUp':
                curPage -= 1

            startPos = (curPage - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            if type == 'mine':
                events = event.objects.filter(updated_by=wechatUser.id)[startPos:endPos]
                if curPage == 1 and allPage == 1:  #标记1
                    allPostCounts = event.objects.filter(updated_by=wechatUser.id).count()
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1
            elif type == 'other':
                evenidtList = participant.objects.filter(partici_user=wechatUser).values_list('event_ID', flat=True).distinct()
                eventsall = []
                for i in evenidtList:
                    eventsall.append(event.objects.get(pk=i))
                events = eventsall[startPos:endPos]

                if curPage == 1 and allPage == 1:  #标记1
                    allPostCounts = len(eventsall)
                    allPage = allPostCounts / ONE_PAGE_OF_DATA
                    remainPost = allPostCounts % ONE_PAGE_OF_DATA
                    if remainPost > 0:
                        allPage += 1

            return render_to_response("list_event.html", {'title': '活动列表', 'user': user, 'events':events, 'allPage':allPage, 'curPage':curPage, 'type': type}, context_instance=RequestContext(rq))
    return HttpResponseRedirect('/welcome/')

# 添加活动
@login_required
@csrf_protect
def add_event(request):
    try:
        userId = request.session["userid"]
        wechatUser = wechat_user.objects.get(pk=userId)
    except:
        return HttpResponseRedirect('/welcome/')

    if request.method == 'GET':
        if wechatUser.wechat_inputname == '':
            form = forms.SetupuserForm(instance=wechatUser)
            return render_to_response('setupinfo.html', {'title': '个人设置', 'form': form}, context_instance=RequestContext(request))

        # 基于活动重新发布功能
        renew = request.GET.get('renew')
        if renew == 'true':
            try:
                eventId = request.GET.get('eventid')
                thisEvent = event.objects.get(pk=eventId)
                eventType = thisEvent.event_type
            except event.DoesNotExist:
                title = u'出错了'
                errorMessage = u'您查询的活动不存在。'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                      context_instance=RequestContext(request))
            form = forms.EventForm(instance=thisEvent)
        else:
            try:
                eventType = request.GET.get('eventtype')
            except:
                eventType = 1
            form = forms.EventForm()
        return render_to_response('addEvent.html', {'title': '新建活动', 'form': form, 'eventtype': eventType},
                              context_instance=RequestContext(request))
    else:
        form = forms.EventForm(request.POST)
        s = datetime.strptime(form.data['eventdate'] + ' ' + form.data['eventtime'], "%Y-%m-%d %H:%M")
        if form.is_valid():
            e = event.objects.create(
                event_title = form.data['event_title'],
                event_detail = form.data['event_detail'],
                event_date = s,
                event_limit = form.data['event_limit'],
                updated_by = userId,
                event_type = form.data['event_type'],
                #updated_date = datetime.now(),
                event_hostfakeID = wechatUser.openid,
                event_hostname = wechatUser.wechat_inputname,
                event_status = 0,
            )
            e.save()

            reMsg = u'发布成功。'
            rqdata = request.GET.copy()
            rqdata['eventid'] = e.id
            rqdata['remsg'] = reMsg
            request.GET = rqdata
            #return showEvent(request)
            return HttpResponseRedirect('/showevent/?eventid='+str(e.id))
        else:
            logger.debug('Setting form is invalid.')
            return render_to_response('addEvent.html', {'title': '新建活动', 'form': form}, context_instance=RequestContext(request))

# 修改活动
@login_required
@csrf_protect
def updateEvent(request):
    try:
        eventId = request.GET.get('eventid')
        thisEvent = event.objects.get(pk=eventId)
    except event.DoesNotExist:
        title = u'出错了'
        errorMessage = u'您查询的活动不存在。'
        return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                              context_instance=RequestContext(request))

    if request.method == 'POST':
        form = forms.EventForm(request.POST, instance=thisEvent)
        if form.is_valid():
            userId = request.session["userid"]
            s = datetime.strptime(form.data['eventdate'] + ' ' + form.data['eventtime'], "%Y-%m-%d %H:%M")
            thisEvent.event_title = form.data['event_title']
            thisEvent.event_detail = form.data['event_detail']
            thisEvent.event_date = s
            thisEvent.event_limit = form.data['event_limit']
            thisEvent.updated_by = userId
            thisEvent.event_status = 0
            thisEvent.event_type = 1
            #thisEvent.updated_date = datetime.now()
            thisEvent.event_hostfakeID = form.data['event_hostfakeID']
            thisEvent.event_hostname = form.data['event_hostname']

            try:
                thisEvent.save()
            except:
                title = u'出错了'
                errorMessage = u'Sorry，出错了。'
                return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                      context_instance=RequestContext(request))

            reMsg = u'更新成功。'
            rqdata = request.GET.copy()
            rqdata['eventid'] = eventId
            rqdata['remsg'] = reMsg
            request.GET = rqdata
            return HttpResponseRedirect('/showevent/?eventid='+eventId)

    return render_to_response('updateEvent.html', {'title': '修改活动', 'form': forms.EventForm(instance=thisEvent), 'eventid': eventId},
                              context_instance=RequestContext(request))

# 活动页面，并展现用户参与情况
@csrf_protect
def showEvent(request):

    # 首先检查COOKIES里面是否已经存在用户信息
    if request.COOKIES.has_key('wxopenid'):
        # 进到这个分支的人，应该是关注了公众号的人。
        # 它们的记录在events中已经建立
        if request.user.is_authenticated():
            try:
                userId = request.session["userid"]
                wechatUser = wechat_user.objects.get(pk=userId)
            except:
                return HttpResponseRedirect('/welcome/')
        else:
            # 客户端会话不会因为退回微信界面而丢失，但服务端重启会造成会话失效。
            openid = request.COOKIES['wxopenid']
            #logger.info('Cookie has openid ' + openid)
            user = authenticate(openid=openid)
            if user is None:
                return HttpResponseRedirect('/welcome/')
            wechatUser = user.real_user
            #logger.debug(wechatUser.id)
            request.session["userid"] = wechatUser.id
            login(request, user)

        if request.GET.get('remsg'):
            remsg = request.GET['remsg']
        else:
            remsg = ''

        try:
            eventId = request.GET.get('eventid')
            thisEvent = event.objects.get(pk=eventId)
        except event.DoesNotExist:
            title = u'出错了'
            errorMessage = u'您查询的活动不存在。'
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                      context_instance=RequestContext(request))

        participantlist = participant.objects.filter(event_ID=eventId)
        eventin = sum(p.partici_type == 1 for p in participantlist)
        eventout = sum(p.partici_type == 0 for p in participantlist)
        eventmaybe = sum(p.partici_type == 2 for p in participantlist)
        numbers = {'eventin': eventin, 'eventout': eventout, 'eventmaybe': eventmaybe}
        userStatus = 5 # 0-不参加，1-参加，2-可能参加，5-未报名，10-活动发起人，100-未关注账号用户
        try:
            thisparticipant = participant.objects.get(event_ID=thisEvent, partici_user=wechatUser)
            userStatus = int(thisparticipant.partici_type)
        except participant.DoesNotExist:
            userStatus = 5

        if wechatUser.id == int(thisEvent.updated_by):
            userStatus = 10

        if thisEvent.event_date < timezone.now():
            thisEvent.event_status = 4
        return render_to_response("showEvent.html", {'title': thisEvent.event_title, 'thisEvent': thisEvent, 'userStatus': userStatus,
                                                    'participantlist': participantlist, "numbers": numbers, 'remsg': remsg,
                                                    'showcomment': 'true', 'useropenid': wechatUser.openid, 'username': wechatUser.wechat_inputname},
                                context_instance=RequestContext(request))

    else:
        if request.GET.get('remsg'):
            remsg = request.GET['remsg']
        else:
            remsg = ''

        try:
            eventId = request.GET.get('eventid')
            thisEvent = event.objects.get(pk=eventId)
        except event.DoesNotExist:
            title = u'出错了'
            errorMessage = u'您查询的活动不存在。'
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                  context_instance=RequestContext(request))

        participantlist = participant.objects.filter(event_ID=eventId)
        eventin = sum(p.partici_type == 1 for p in participantlist)
        eventout = sum(p.partici_type == 0 for p in participantlist)
        eventmaybe = sum(p.partici_type == 2 for p in participantlist)
        numbers = {'eventin': eventin, 'eventout': eventout, 'eventmaybe': eventmaybe}
        userStatus = 100  # 0-不参加，1-参加，2-可能参加，5-未报名，10-活动发起人，100-未关注账号用户

        return render_to_response("showEvent.html", {'title': thisEvent.event_title, 'thisEvent': thisEvent, 'userStatus': userStatus,
                                                     'participantlist': participantlist, "numbers": numbers, 'remsg': remsg,
                                                    'showcomment': 'false', 'useropenid': '', 'username': ''},
                                  context_instance=RequestContext(request))

# 响应按钮事件：报名、修改事件状态
@login_required
@csrf_protect
def joinEvent(request):
    if request.user.is_authenticated():
        reMsg = ''
        try:
            userId = request.session["userid"]
            wechatUser = wechat_user.objects.get(pk=userId)
        except:
            return HttpResponseRedirect('welcome.html')

        if wechatUser.wechat_inputname=='':
            form = forms.SetupuserForm(instance=wechatUser)
            return render_to_response('setupinfo.html', {'title': '个人设置', 'form': form})

        try:
            eventId = request.GET.get('eventid')
            jointype = request.GET.get('jointype')
            thisEvent = event.objects.get(pk=eventId)
        except event.DoesNotExist:
            title = u'出错了'
            errorMessage = u'您查询的活动不存在。'
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                                  context_instance=RequestContext(request))

        #partici_type: 0-不参加，1-参加，2-可能参加，5-未报名，10-活动发起人
        participantlist = participant.objects.filter(event_ID=eventId)
        eventin = sum(p.partici_type == 1 for p in participantlist)
        eventout = sum(p.partici_type == 0 for p in participantlist)
        eventmaybe = sum(p.partici_type == 2 for p in participantlist)
        try:
            thisparticipant = participant.objects.get(event_ID=thisEvent, partici_user=wechatUser)
        except:
            thisparticipant = participant()

        if jointype == 'stop':
            thisEvent.event_status = 3
            thisEvent.save()
        elif jointype == 'cancel':
            thisEvent.event_status = 2
            thisEvent.save()
        elif jointype == 'join':
            if thisEvent.event_limit > eventin:
                thisparticipant = participant(pk=thisparticipant.id, partici_fakeID='', event_ID=thisEvent, event_sn=thisEvent.event_sn,
                                              partici_name=wechatUser.wechat_inputname, partici_type=1,
                                              register_time=datetime.now(), partici_user=wechatUser, partici_openid=wechatUser.openid)
                thisparticipant.save()
                if thisEvent.event_limit <= ++eventin:
                    thisEvent.event_status = 1
                    thisEvent.save()
                reMsg = u'报名成功。'
            else:
                reMsg = u'此活动已报名人满。'
        elif jointype == 'maybe':
            thisparticipant = participant(pk=thisparticipant.id, partici_fakeID='', event_ID=thisEvent, event_sn=thisEvent.event_sn,
                                          partici_name=wechatUser.wechat_inputname, partici_type=2,
                                          register_time=datetime.now(), partici_user=wechatUser, partici_openid=wechatUser.openid)
            thisparticipant.save()
            reMsg = u'报名成功。'
        elif jointype == 'notjoin':
            thisparticipant = participant(pk=thisparticipant.id, partici_fakeID='', event_ID=thisEvent, event_sn=thisEvent.event_sn,
                                          partici_name=wechatUser.wechat_inputname, partici_type=0,
                                          register_time=datetime.now(), partici_user=wechatUser, partici_openid=wechatUser.openid)
            thisparticipant.save()
            reMsg = u'报名成功。'

        rqdata = request.GET.copy()
        rqdata['eventid'] = eventId
        rqdata['remsg'] = reMsg
        request.GET = rqdata
        return showEvent(request)

    else:
        return HttpResponseRedirect("/welcome/")

# 处理消息机制，应该是公众平台中最核心的处理部分
import hashlib
from lxml import etree
from messages import processMessage
from eventmsgs import processEventMessage

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
                event_msg = msg_in.find('Event')
                if event_msg==None : #这是一个消息
                    return processMessage(msg_in)
                else: #这是一个事件消息
                    return processEventMessage(msg_in,event_msg)
        else:
            logger.info('Illedge message received')
            raise Http404
    except Exception as e: # 此处仅保留，实际情况是无需进行任何处理。
        logger.info('Exception received: ' + e.message)
        raise e

@csrf_protect
def setting(request):
    if request.method=='GET':
        if request.GET.has_key('openid'):
            openid = request.GET['openid']
            logger.debug('Request has openid ' + openid)
            max_age = 365 * 24 * 60 * 60

            user = authenticate(openid=openid)
            if user is not None:
                real_user = user.real_user
                logger.debug(real_user.id)
                login(request, user)
                request.session['userid'] = real_user.id
                #request.COOKIES

                form = forms.SetupuserForm(instance=real_user)
                response = render_to_response('setupinfo.html', {'title': '个人设置', 'form': form}, context_instance=RequestContext(request))
                response.set_cookie("wxopenid", openid, max_age=max_age)
                return response

            else:
                logger.error("Can't find user " + openid)
                return render_to_response('welcome.html')

        else:
            return render_to_response('welcome.html')
            #return HttpResponseRedirect('/')

    else: #POST
        if not request.user.is_authenticated:
            return render_to_response('welcome.html')
        else:
            userid = request.session['userid']

        form = forms.SetupuserForm(request.POST)
        if form.is_valid():
            try:
                wechatUser = wechat_user.objects.get(pk=userid)
            except wechat_user.DoesNotExist:
                return HttpResponseRedirect('/welcome/')

            #assert user.openid==userid
            wechatUser.wechat_inputname = form.data['wechat_inputname']
            wechatUser.initialized = True
            wechatUser.save()

            title = u'设置成功'
            errorMessage = u'个人信息设置成功，现在您可以返回并发布或参与活动了！'
            return render_to_response("errorMessage.html", {'errorMessage': errorMessage, 'title': title},
                              context_instance=RequestContext(request))
        else:
            logger.debug('Setting form is invalid.')
            return render_to_response('setupinfo.html', {'title': '个人设置', 'form': form},
                context_instance=RequestContext(request))

import urllib
def oauth(request):
    state = request.GET.get('state','state')
    if state is not 'state':
        code = request.session['code'] = request.GET['code']
        logger.debug('Received a code: ' + code)

        # 利用code从服务器获取用户信息，并将这个用户信息保存到session中去。
        if state=='FoperateWX':
            userinfo = get_wx_info(code, request.session)
        else:
            userinfo = get_qq_info(code, request.session)

        # 使用新的认证后台来代替现有的后台
        if userinfo is not None:
            user = authenticate(openid = userinfo['openid'])
            request.session['userid'] = user.real_user.id
            login(request, user)
            if request.session.has_key('url'):
                url = request.session['url']
                del request.session['url']
            else:
                url = '/'
            return HttpResponseRedirect(url)
        else:
            return render_to_response('welcome.html')
    else:
        return render_to_response('oauth.html',{'title','自动认证'})

APP_ID='100561618'
APP_KEY='dbbea5729ffd5182deff63f90131bc3b'
WX_APP_ID='wx8763ead7d4408241'
WX_APP_KEY='4042d9f53dfa2abfdd542af803116787'
def check_auth(request):

    '''next = request.GET.get('next','/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(next)

    # 首先检查COOKIES里面是否已经存在用户信息
    if request.COOKIES.has_key('wxopenid'):
        # 进到这个分支的人，应该是关注了公众号的人。
        # 它们的记录在events中已经建立
        openid = request.COOKIES['wxopenid']
        user = authenticate(openid=openid)
        if user is not None:
            real_user = user.real_user
            request.session['userid'] = real_user.id
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            return HttpResponse(status=500)
    else:
        if next.startswith('/moveuser/'):
            # 暂时不要后面的处理
            return render_to_response('welcome.html')
        else:
            url = 'http://whitemay.pythonanywhere.com/moveuser/?' + urllib.urlencode({
                'dest':next
            })
            return HttpResponseRedirect(url)

    # 然后启动OAuth2过程，在这里需要判断启动谁
    #url = request.build_absolute_uri()
    #logger.debug(url)
    request.session['url'] = next'''

    useragent = request.META['HTTP_USER_AGENT']
    logger.debug(useragent)
    if 'MicroMessenger' in useragent:
        auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' + \
            urllib.urlencode({
                'response_type':'code',
                'appid':WX_APP_ID,
                'redirect_uri':'http://www.eztogether.net/oauth/',
                'scope':'snsapi_base',
                #'state':'Foperate',
            }) + '&state=FoperateWX#wechat_redirect'
    else:
        auth_url = 'https://graph.qq.com/oauth2.0/authorize?' + \
            urllib.urlencode({
                'response_type':'code',
                'client_id':APP_ID,
                'redirect_uri':'http://www.eztogether.net/oauth/',
                'state':'FoperateQQ',
            })
    logger.debug(auth_url)
    return HttpResponseRedirect(auth_url)

from urlparse import parse_qs
import json
def get_qq_info(code, session):
    url = 'http://https://graph.qq.com/oauth2.0/token?' + urllib.urlencode({
        'grant_type':'authorization_code',
        'client_id':APP_ID,
        'client_secret':APP_KEY,
        'code':code,
        'redirect_uri':'http://www.eztogether.net/oauth',
    })
    f = urllib.urlopen(url)
    text = f.read()
    f.close()
    logger.debug('Thread return: ' + text)
    q = parse_qs(text)
    if q.has_key('access_token'):
        token = q['access_token'][0]
        logger.debug('Get token: ' + token)
        session['token'] = token
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + token
        f = urllib.urlopen(url)
        text = f.read()
        f.close()
        logger.debug('Thread return 2: ' + text)
        jobj = None
        if text.strtwith('callback('):
            jobj = json.loads(text[9:-1])
            if jobj.has_key('openid'):
                session['openid'] = jobj['openid']
        return jobj

def get_wx_info(code, session):
    #https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' + urllib.urlencode({
        'grant_type':'authorization_code',
        'appid':WX_APP_ID,
        'secret':WX_APP_KEY,
        'code':code,
        'redirect_uri':'http://www.eztogether.net/oauth/',
    })
    f = urllib.urlopen(url)
    jobj = json.load(f)
    f.close()
    logger.debug('Thread return: ' + str(jobj))
    if jobj.has_key('errmsg'):
        logger.error('WX get error: ' + jobj['errmsg'])
        return None
    session['access_token'] = jobj['access_token']
    session['refresh_token'] = jobj['refresh_token']
    session['openid'] = jobj['openid']
    return jobj

def welcome(request):
    return render_to_response('welcome.html')

def test(request):
    return render_to_response('test.html')

# 根据传递过来的参数设置openid以及设定转向
def cookie_openid(request):
    try:
        next = request.GET['next']
        response = HttpResponseRedirect(next)

        openid = request.GET['openid']
        logger.debug('Request has openid ' + openid)
        max_age = 365 * 24 * 60 * 60

        response.set_cookie("wxopenid", openid, max_age=max_age)
        return response
    except:
        raise render_to_response('welcome.html')

@login_required
def move_user(request):
    logger.debug("Move User")
    try:
        openid = request.COOKIES['wxopenid']
        next = request.GET['dest']
        url = "http://www.eztogether.net/setcookie/?" + urllib.urlencode({
            'openid':openid,
            'next':next,
        })
        return HttpResponseRedirect(url)
    except:
        return render_to_response('welcome.html')
