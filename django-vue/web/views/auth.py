from django.http import *
from django.shortcuts import render,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')

    logout(request)
    username = password = ''

    if request.POST and all(k in request.POST for k in ('username', 'password')):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            # change
            return HttpResponseRedirect('/avatar')
            #
        return render(request, 'arc/index.html', {'error_message': 'ID/kata laluan tidak betul'})

    return render(request, 'arc/index.html')

#@login_required(login_url='/login/')
#def main(request):
#    ....