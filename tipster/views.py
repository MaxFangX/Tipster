from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from tipster.models import Post, Profile, Upvote


def index(request):
    posts = Post.objects.order_by('created_at')[:25]
    profile = Profile.objects.get(user=request.user)
    return render_to_response(
        template_name='index.html',
        context={'posts': posts, 'user': request.user, 'profile': profile})


def login(request):
    return render_to_response(
        template_name='login.html',
        context={})


def buy(request):
    return render_to_response(
        template_name='buy.html',
        context={})


def profile(request, username):
    user = User.objects.get(username='phlip9')
    profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='profile.html',
        context = {'user': user, 'profile': profile})


def cashout(request):
    print('cashout')


def coinbase(request):
    # receive payment for some upvotes
    print(request)


def upvote(request, pk):

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    post = Post.objects.get(id=pk)
    existing_upvotes = Upvote.objects.filter(post=post).count()
    amount = int(request.GET.get('amount', 0))
    Upvote(post=post,
           user=request.user,
           index=existing_upvotes + 1,
           amount=amount).save()

    return HttpResponseRedirect("/")
