from django import template
from django.shortcuts import render_to_response
from tipster.models import *

def index(request):
    posts = Post.objects.order_by('created_at')[:25]
    user = User.objects.get(username='phlip9')
    print(posts[0].created_at)
    _profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='index.html',
        context={ 'posts': posts, 'user': user, 'profile': _profile })

def login(request):
    return render_to_response(
        template_name='login.html',
        context={})

def buy(request):
    return render_to_response(
        template_name='buy.html',
        context={})

def profile(request, username):
    user = {
        'username': 'phlip9',
        'upvotes': 25
    }
    profile = {
        'username': 'phlip9'
    }
    return render_to_response(
        template_name='profile.html',
        context={ 'user': user, 'profile': profile })

def cashout(request):
    print('cashout')

def coinbase(request):
    # receive payment for some upvotes
    print(request)
