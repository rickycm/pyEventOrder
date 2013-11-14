#coding=utf-8
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate, login
from pyEventOrderWeb import forms
from django.template import RequestContext
from pyEventOrderWeb.models import *

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
        if request.user.is_authenticated():
            user = request.user
            return render_to_response("index.html", {'user': user}, context_instance=RequestContext(request))
        return HttpResponseRedirect("/accounts/login/")

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

