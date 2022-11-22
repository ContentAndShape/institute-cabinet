from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required(login_url="/login/")
def cabinet(request: HttpRequest) -> HttpResponse:

    context = {
        'user': request.user,
        'user_type': request.user.__class__.__name__,
    }
    return render(request, 'usr_cabinet/base_cabinet.html', context)
