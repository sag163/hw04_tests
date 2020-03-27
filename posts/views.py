from django.shortcuts import get_object_or_404, render, redirect
from posts.models import Post
from group.models import Group
from .forms import PostForm
from django.core.paginator import Paginator
from users.forms import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {"page": page, 'paginator':paginator})


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]  
    return render(request, "group.html", {"group": group, "posts": posts})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()
        return render(request, "new.html", {"form": form})

def profile(request, username):
    persons = Post.objects.filter(author__username=username)
    paginator = Paginator(persons, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count_post = Post.objects.filter(author__username=username).count()
    author = User.objects.get(username=username)
    profile_dict = {"page": page, 'paginator':paginator, 'username':username, 'count_post':count_post, 'author':author}
    return render(request, "profile.html", profile_dict)

def post_view(request, username, post_id):
    post_user = Post.objects.filter(author__username=username).filter(pk=post_id)
    count_post = Post.objects.filter(author__username=username).count()  
    return render(request, "post.html", {'post_user':post_user, 'username':username, 'count_post':count_post, 'post_id':post_id})

def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        print("qwerty")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print("qwerty")
            return redirect("profile", username)
    else:
        form = PostForm(instance=post) 
        print("qwerty")
        return render(request, "new.html", {"form": form, 'post':post})