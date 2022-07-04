from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .models import (
    Faculty,
)


class EmailModelBackend(ModelBackend) :

    # user = authenticate(username, password)

    def authenticate(self, request, username=None, password=None, **kwargs) :
        
        if '@' in username :
            kwargs = {'email': username}
        else :
            print("No @ in username")
            return None


        if password is None :
            print("password is None")
            return None

        
        try :
            user = User.objects.get(**kwargs)

        except User.DoesNotExist :
            print("User does not exist")
            # User.set_password(password)

        else :
            if user.check_password(password) and self.user_can_authenticate(user) :
                print("success custom authenticate")
                return user
            print("failure custom authenticate")