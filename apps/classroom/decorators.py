from django.shortcuts import redirect

def verify_user_is_staff(redirect_url_name):
    def wrapper(f):
        def wrapped(request, pk):
            if not request.user.is_staff:
                return redirect(redirect_url_name, pk)
            return f(request, pk)
        return wrapped
    return wrapper
