from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import PostForm


POSTS_COUNT = 10


def authorized_only(func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')
    return check_user


# Главная страница
def index(request):
    posts = Post.objects.select_related('author', 'group')[:POSTS_COUNT]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


# Страница со списком опубликованных постов
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


# Здесь код запроса к модели и создание словаря контекста
def profile(request, username):
    author_name = get_object_or_404(User, username=username)
    post_list = author_name.posts.all()
    paginator = Paginator(post_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_amount = paginator.count
    context = {
        'author': author_name,
        'page_obj': page_obj,
        'posts_amount': posts_amount,
    }
    return render(request, 'posts/profile.html', context)


# Здесь код запроса к модели и создание словаря контекста
def post_detail(request, post_id):
    full_post = get_object_or_404(Post, pk=post_id)
    title = full_post.text
    author_posts = Post.objects.filter(author=full_post.author)
    posts_amount = author_posts.count()
    context = {
        'title': title,
        'post': full_post,
        'posts_amount': posts_amount,
    }
    return render(request, 'posts/post_detail.html', context)


@authorized_only
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('posts:profile', form.author)
    form = PostForm()
    template = 'posts/post_create.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@authorized_only
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm(instance=post)
        template = 'posts/post_create.html'
        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
        }
    return render(request, template, context)
