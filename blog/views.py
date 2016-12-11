from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_post = Post.objects.filter(user=request.user)
                posts = all_post.order_by('-date')[:2]

                return render(request, 'blog/index.html', {'posts':posts})

    return render(request, 'blog/register.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                all_post = Post.objects.filter(user=request.user)
                posts = all_post.order_by('-date')[:2]

                return render(request, 'blog/index.html', {'posts': posts})
            else:
                return render(request, 'blog/login.html', {'error_message': 'Your Account has been disabled.'})

        return render(request, 'blog/login.html', {'error_message': 'Username or Password is invalid.'})

    return render(request, 'blog/login.html')


def user_logout(request):
    logout(request)
    form = UserForm(request.POST or None)

    return render(request, 'blog/login.html', {'form':form})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        all_post = Post.objects.filter(user=request.user)
        query = request.GET.get('q')
        if query:
            posts = all_post.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            ).distinct()

            if posts:
                return render(request, 'blog/index.html', {'posts': posts})
            else:
                context = {
                    'error_message': 'No result for the query.Please try searching something else.'
                }
                return render(request, 'blog/index.html', context)

        posts = all_post.order_by('-date')[:2]
        return render(request, 'blog/index.html', {'posts': posts})


def archive(request):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        all_post = Post.objects.filter(user=request.user)
        all_post = all_post.order_by('-date')[:25]
        return render(request, 'blog/archive.html', {'all_post':all_post})


def detail(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        return render(request, 'blog/post.html', {'post': post, 'user':user})


def create_post(request):
    if not request.user.is_authenticated():
        return render(request, 'blog/login.html')
    else:
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return render(request, 'blog/post.html', {'post': post})

        return render(request, 'blog/post_form.html', {'form': form})


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    all_post = Post.objects.filter(user=request.user)
    return render(request, 'blog/archive.html', {'all_post': all_post})