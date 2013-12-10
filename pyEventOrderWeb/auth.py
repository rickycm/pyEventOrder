#coding=utf-8
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from models import wechat_user

logger = logging.getLogger('django.dev')

class OAuthBackend(object):

    def authenticate(self, openid=None, userinfo=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get_by_natural_key('user')
        except User.DoesNotExist:
            user = User.objects.create(username='user', is_active=True)
            user.save()

        if openid is not None:
            try:
                _user = wechat_user.objects.get(openid=openid)
                _user.save()
                user.real_user = _user
                return user
            except wechat_user.DoesNotExist:
                return None

        elif userinfo is not None:
            # 新用户驾到
            openid = userinfo.pop('openid')
            _user, created = wechat_user.objects.get_or_create(openid=openid)
            for attr, val in userinfo.items():
                if hasattr(_user, attr):
                    setattr(_user, attr, val)
            _user.save()
            user.real_user = _user
            return user

        return None


    def get_user(self, user_id):
        UserModel = get_user_model()
        #logger.debug('OAuthBackend get user: ' + str(user_id))
        return UserModel._default_manager.get(pk=user_id)