from django.shortcuts import redirect

class verify_user_is_staff(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, request, pk):
        if not request.user.is_staff:
            return redirect('show_classroom', pk)
        return self.f(request, pk)
