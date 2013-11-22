#coding=utf-8
import logging

from django.contrib.auth import get_user_model

from models import wechat_user


logger = logging.getLogger('django.dev')

class OAuthBackend(object):

    def authenticate(self, openid=None, userinfo=None, **kwargs):
        UserModel = get_user_model()
        user = UserModel._default_manager.get_by_natural_key('user')
        if openid is not None:
            try:
                _user = wechat_user.objects.get(openid=openid)
                user.real_user = _user
                return user
            except wechat_user.DoesNotExist:
                return None

        elif userinfo is not None:
            # 新用户驾到
            _user = wechat_user.objects.create(openid=userinfo['openid'], subscribe=False, initialized=False)
            _user.save()
            user.real_user = _user
            return user

        return None


    def get_user(self, user_id):
        UserModel = get_user_model()
        #logger.debug('OAuthBackend get user: ' + str(user_id))
        return UserModel._default_manager.get(pk=user_id)