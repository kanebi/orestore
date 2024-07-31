from django.shortcuts import render

# Create your views here.


def index(request):
    return render (request, 'index.html')

def user_profile(request):
    return render (request, 'core/profile.html')
