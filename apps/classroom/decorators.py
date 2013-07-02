from django.shortcuts import redirect

<<<<<<< HEAD
class verify_user_is_staff(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, request, pk):
        if not request.user.is_staff:
            return redirect('show_classroom', pk)
        return self.f(request, pk)
=======
def verify_user_is_staff(redirect_url_name):
    def wrapper(f):
        def wrapped(request, pk):
            if not request.user.is_staff:
                return redirect(redirect_url_name, pk)
            return f(request, pk)
        return wrapped
    return wrapper
>>>>>>> a9e833f86e0b972cfda2ca08e030ad60ab7b5bac
