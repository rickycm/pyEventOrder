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

def login_form(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            form = forms.LoginForm(request.POST)
            login(request, user)
            # Redirect to a success page.
            return render_to_response("index.html", {'user':user})
            #return HttpResponseRedirect("/")
        else:
            form = forms.LoginForm()
            # Return an error message.
            return render_to_response("login.html", {'msg':"请重新输入账户", 'form':form}, context_instance=RequestContext(request))
    except:
        form = forms.LoginForm()
        return render_to_response("login.html", {'msg':"请重新登录", 'form':form}, context_instance=RequestContext(request))


def register(request):
        form = UserCreationForm()
        if request.method == 'GET':
                return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        new_user = form.save()
                        return HttpResponseRedirect("/")

def index(request):
        if request.user.is_authenticated():
                return render_to_response("index.html",{'name':request.user.username})
        return HttpResponseRedirect("/accounts/login/")