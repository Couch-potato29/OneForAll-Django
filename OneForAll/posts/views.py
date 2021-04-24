from django.core.checks import messages
from django.http import request
from profiles.models import Profiles
from django.shortcuts import render, redirect
from .models import Post,Like
from django.urls import reverse_lazy
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

@login_required
def post_create_list_view(request):
    queryset = Post.objects.all()
    profile = Profiles.objects.get(user=request.user)

    p_form = PostModelForm()
    c_form = CommentModelForm()
    posted = False

    profile = Profiles.objects.get(user=request.user)

    if 'submit_post' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            posted = True

    if 'submit_comment' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            post_id = request.POST.get('post_id')
            instance.post = Post.objects.get(id=post_id)
            instance.save()
            c_form = CommentModelForm()

    context = {
        'queryset':queryset,
        'profile' : profile,
        'p_form' : p_form,
        'c_form' : c_form,
        'posted' : posted,
    }

    return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profiles.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id = post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value='Like'

        post_obj.save()
        like.save()

        data = {
            'value':like.value,
            'likes':post_obj.liked.all().count()
        }
    
    return redirect('posts:main_post_view')

class PostDeleteView(LoginRequiredMixin ,DeleteView):
    model = Post
    template_name = 'posts/are_you_sure.html'
    success_url = reverse_lazy('posts:main_post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk = pk)
        if not obj.author.user==self.request.user:
            messages.warning(self.request, "You do not have the permission to delete this post since you have not uploaded it")
        return obj

class PostUpdateView(LoginRequiredMixin ,UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/edit_post.html'
    success_url = reverse_lazy('posts:main_post_view')

    def form_valid(self, form):
        profile = Profiles.objects.get(user = self.request.user)

        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You do not have the permission to edit this post since you have not uploaded it")
            return super().form_invalid(form)