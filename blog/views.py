from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template.context_processors import csrf

from .models import Post, Comments
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import LoginForm, RegisterForm,PostForm
from django.utils import timezone
import time


def index(request):
    latest_post = Post.objects.order_by('-published_date')[:10]
    context = {'latest_post': latest_post}
    return render(request, 'blog/index.html', context)


def all(request):
    latest_post = Post.objects.order_by('-published_date')
    context = {'latest_post': latest_post}
    return render(request, 'blog/all.html', context)


def post(request, post_id):# переделать под условие
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

    posts = Post.objects.all()
    datas= {}
    for post in posts:
        date=post.published_date
        date2=date.strftime("%B")
        datas.update({date2:post})
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

def new_post(request):
    if request.POST:
        author = User.objects.get(id=request.user.id)
        entry = Post(author=author, title = request.POST['title'], text = request.POST['text'], published_date = timezone.now())
        entry.save()
        return redirect('/')
    else:
        return render(request, 'blog/newpost.html')
    return render(request, 'blog/newpost.html')
def lk(request):
    # nick=User.objects.get(username=request.user)
    latest_post = Post.objects.filter(author_id=request.user.id)

    comments = Comments.objects.filter(author=request.user)
    # print ("ID",nick.id)
    # print ("POSTS", latest_post.title)

    context = {'latest_post': latest_post, 'comments': comments}
    return render(request, 'blog/lk.html', context)
