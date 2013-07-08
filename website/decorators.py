from django.shortcuts import redirect

def verify_user_is_staff(redirect_url_name):
    def wrapper(f):
        def wrapped(request, classroom_pk, *args, **kwargs):
            if not request.user.is_staff:
                return redirect(redirect_url_name, classroom_pk)
            return f(request, classroom_pk, *args, **kwargs)
        return wrapped
    return wrapper


def verify_user_is_active(redirect_url_name):
    def wrapper(f):
        def wrapped(request, classroom_pk, *args, **kwargs):
            if not request.user.is_active:
                return redirect(redirect_url_name, classroom_pk)
            return f(request, classroom_pk, *args, **kwargs)
        return wrapped
    return wrapper
