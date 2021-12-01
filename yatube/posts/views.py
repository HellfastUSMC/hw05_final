from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from . import forms
from .models import Following, Group, Post

User = get_user_model()


def index(request):
    template = 'posts/index.html'
    page_title = 'Главная страница Yatube'
    title = 'Последние обновления на сайте'
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title,
        'page_title': page_title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    title = group.title
    page_title = title
    posts = group.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group_slug': slug,
        'page_obj': page_obj,
        'group_title': title,
        'page_title': page_title,
        'group': group
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user_c = get_object_or_404(User, username=username)
    posts = user_c.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_total = posts.count()
    user_name = f'{user_c.first_name} {user_c.last_name}'
    title = f'Профайл пользователя {user_name}'
    following = False
    print(request.user.following.filter(), request.user.username)
    for author in request.user.following.all():
        if user_c == User.objects.get(username=author):
            following = True
    context = {
        'title': title,
        'page_obj': page_obj,
        'posts_total': posts_total,
        'user_name': user_name,
        'author': user_c,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    group = post.group
    author = f'{post.author.first_name} {post.author.last_name}'
    date = post.pub_date
    posts_count = post.author.posts.count()
    title = f'Пост {post.text[:30]}'
    username = post.author.username
    post_author = post.author
    text = post.text
    comments = post.comments
    form = form = forms.CommentForm(request.POST or None)
    context = {
        'title': title,
        'author': author,
        'group': group,
        'date': date,
        'posts_count': posts_count,
        'username': username,
        'text': text,
        'post_id': post_id,
        'post': post,
        'post_author': post_author,
        'comments': comments,
        'form': form
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = forms.PostForm(request.POST or None, request.FILES)
    if not form.is_valid():
        context = {
            'form': form,
            'request': request,
        }
        return render(request, template, context)
    else:
        form_obj = form.save(commit=False)
        form_obj.author = request.user
        form_obj.save()
        return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id)
    template = 'posts/create_post.html'
    form = forms.PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post_obj,
    )
    context = {
        'is_edit': True,
        'form': form
    }
    if request.user != post_obj.author:
        return redirect('posts:post_detail', post_id=post_id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    else:
        return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = forms.CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    page_title = 'Лента подписок'
    title = 'Лента подписок'
    posts = Post.objects.order_by('-pub_date').filter(author=request.user)
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    subs = [author for author in request.user.following.all()]
    print('!!! -', subs)
    print(request.user.follower.all(), request.user.following.all(), Following.objects.filter(author))
    context = {
        'page_obj': page_obj,
        'title': title,
        'page_title': page_title,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    Following.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Following.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
