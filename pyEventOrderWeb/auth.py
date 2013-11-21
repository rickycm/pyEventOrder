from django.contrib.auth import get_user_model

class OAuthBackend(object):

    def authenticate(self, code):
        UserModel = get_user_model()
        user = UserModel._default_manager.get_by_natural_key('user')
        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        return UserModel._default_manager.get_by_natural_key(pk=user_id)