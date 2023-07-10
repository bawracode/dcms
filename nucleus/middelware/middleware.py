
import threading

_thread_locals = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        return self.get_response(request)

def get_current_request():
    return getattr(_thread_locals, 'request', None)




# middleware.py
from molecules.language.models import Profile
from django.utils import translation

class AdminLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # chech if table is empty then set language to english
            if Profile.objects.count() == 0:
                profile = Profile.objects.create(user=request.user, language='en')
                profile.save()
            # create profile if not exist
            if not Profile.objects.filter(user=request.user).exists():
                profile = Profile.objects.create(user=request.user, language='en')
                profile.save()
            profile = Profile.objects.get(user=request.user)
            language = profile.language
           

            translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

        
        return self.get_response(request)



