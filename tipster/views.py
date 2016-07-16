from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from tipster.models import Post, Profile


def index(request):
    posts = Post.objects.all()[:25]
    posts = sorted(posts, key=lambda p: p.value, reverse=True)
    context = {'posts': posts, 'user': request.user, }
    if request.user.is_authenticated():
        _profile = Profile.objects.get(user=request.user)
        context['profile'] = _profile
    return render_to_response(
        template_name='index.html',
        context=context)


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
    _profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='profile.html',
        context = {'user': user, 'profile': _profile})


def cashout(request):
    print('cashout')


def coinbase(request):
    # receive payment for some upvotes
    print(request)


def upvote(request, pk):
    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    post = Post.objects.get(id=pk)
    amount = int(request.GET.get('amount', 0))
    post.upvote(request.user, amount)

    return HttpResponseRedirect("/")


def create_post(request):
    if not request.user.is_authenticated():
        raise Exception("Must be logged in to post")

    title = request.GET.get('title', "(No title)")
    link = request.GET.get('link', "http://maxfa.ng")

    p = Post(curator=request.user,
             title=title,
             link=link)
    p.save()
    p.upvote(request.user, 100)  # Costs 100 satoshi to post

    return HttpResponseRedirect("/")

def submit(request):
    user = User.objects.get(username='phlip9')
    _profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='submit.html',
        context={ 'user': user, 'profile': _profile })
