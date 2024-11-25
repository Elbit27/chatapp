from django.contrib.auth import login
from django.shortcuts import render, redirect
from account.serializers import UserRegisterSerializer
def frontpage(request):
    return render(request, 'core/frontpage.html')
