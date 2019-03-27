from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template.context_processors import csrf

from .models import Post, Comments
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import LoginForm, RegisterForm


def index(request):
    latest_post = Post.objects.order_by('-published_date')[:10]
    context = {'latest_post': latest_post}
    return render(request, 'blog/index.html', context)


def all(request):
    latest_post = Post.objects.order_by('-published_date')
    context = {'latest_post': latest_post}
    return render(request, 'blog/all.html', context)


def post(request, post_id):
    try:
        title = Post.objects.get(id=post_id)
        author = User.objects.get(id=request.user.id)

        text = request.POST['comment']
        comment = Comments(title=title, author=author, text=text)
        comment.save()
    except:
        pass

    post = Post.objects.get(pk=post_id)
    comments = post.comments_set.all()
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/detail.html', context)


def history(request):
    # user = User.objects.get(id=request.user.id)
    posts = Post.objects.all()
    datas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # datas = {'01':'1', '02':'1', '03':'1', '04':'1', '05':'1', '06':'1', '07':'1', '08':'1', '09':'1', '10':'1', '11':'1', '12':'1'}
    context = {'posts': posts, 'datas': datas}
    return render(request, 'blog/history.html', context)


def render_to_respose(param, args):
    pass


def signin(request):
    args = {}
    args.update(csrf(request))
    args['form'] = LoginForm(request.POST)
    if request.POST:
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            args['signin_error'] = 'WRONG NICKNAME OR PASSWORD !'
            return render(request, 'blog/signin.html', args)
    else:
        return render(request, 'blog/signin.html', args)


def signout(request):
    logout(request)
    return redirect('blog:index')

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegisterForm()
    if request.POST:
        user = RegisterForm(request.POST)
        try:
            user_exists = User.objects.get(username = request.POST['login'])
        except:
            user_exists = False
        if user_exists is False:
            if user.is_valid():
                user = User.objects.create_user(username=request.POST['login'], email=request.POST['email'], password=request.POST['password'])
                user.save()
                user = authenticate(username=request.POST['login'], password=request.POST['password'])
                login(request, user)
                return redirect('/')
            else:
                args['register_error'] = 'Wrong email !'
                return render(request, 'blog/register.html', args)
        else:
            args['register_error'] = 'User already exists !'
            return render(request, 'blog/register.html', args)
    return render(request, 'blog/register.html', args)