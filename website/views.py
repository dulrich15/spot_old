from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect


class TextPlainView(TemplateView):
  def render_to_response(self, context, **kwargs):
    return super(TextPlainView, self).render_to_response(
      context, content_type='text/plain', **kwargs)

def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def user_login(request):
    post = request.POST['password'].lower()
    user = None
    
    # see http://stackoverflow.com/questions/4754980/how-to-manually-authenticate-after-get-django-user
    if post in ['dave', 'test']:
        user = User.objects.get(username=post)
        user.backend = 'django.contrib.auth.backends.ModelBackend' 
        
    if user and user.is_active:
        login(request, user)
        
    return redirect(request.META.get('HTTP_REFERER', '/')) 
