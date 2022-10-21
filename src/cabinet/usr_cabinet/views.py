from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def cabinet(request: HttpRequest) -> HttpResponse:

    if request.user.is_authenticated == False:
        return redirect("login/")

    context = {
        'user': request.user,
        'user_type': request.user.__class__.__name__,
    }
    return render(request, 'usr_cabinet/base_cabinet.html', context)
