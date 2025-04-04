from django.shortcuts import render , redirect
from django.contrib.auth import logout # type: ignore
def user_logout(request):
    logout(request)
    return redirect('login')


