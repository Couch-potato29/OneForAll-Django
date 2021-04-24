from django.contrib.auth import login
from django.shortcuts import render, resolve_url,redirect,get_object_or_404
from django.utils import tree
from .models import Profiles, Relationship
from .forms import ProfileForm
from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

@login_required
def profile_view(request):
    obj = Profiles.objects.get(user = request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=obj)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': obj,
        'form' : form,
        'confirm' : confirm
    }

    return render(request, 'profiles/myprofile.html', context)

class ProfileDetailsView(LoginRequiredMixin ,DetailView):
    model = Profiles
    template_name = 'profiles/profile_detail.html'

    # def get_object(self, slug=None):
    #     slug = self.kwargs.get('slug')
    #     #id = self.kwargs.get('id')
    #     profile = Profiles.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profiles.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for rel in rel_r:
            rel_receiver.append(rel.receiver.user)
        for rel in rel_s:
            rel_sender.append(rel.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_posts()
        context['no_posts'] = True if len(self.get_object().get_posts()) > 0 else False 

        return context

@login_required
def requests_received_view(request):
    profile = Profiles.objects.get(user = request.user)
    queryset = Relationship.objects.requests_received(profile)

    result = list(map(lambda x:x.sender, queryset))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {'qs':result,
                'is_empty':is_empty}

    return render(request, 'profiles/my_requests.html', context)

@login_required
def request_profiles_list_view(request):
    user = request.user
    qs = Profiles.objects.get_profiles_to_request(user)

    context = {'qs':qs}

    return render(request, 'profiles/to_invite_list.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profiles.objects.get_all_profiles(user)

    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

class ProfileListView(LoginRequiredMixin ,ListView):
    model = Profiles
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profiles.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profiles.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for rel in rel_r:
            rel_receiver.append(rel.receiver.user)
        for rel in rel_s:
            rel_sender.append(rel.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def send_requests(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profiles.objects.get(user = user)
        receiver = Profiles.objects.get(pk = pk)
        rel = Relationship.objects.create(sender = sender, receiver = receiver, status = 'sent')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:myprofile')

@login_required
def remove_connection(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profiles.objects.get(user = user)
        receiver = Profiles.objects.get(pk = pk)

        rel = Relationship.objects.get(
            (Q(sender = sender) & Q(receiver = receiver))|
            (Q(sender=receiver) & Q(receiver = sender)))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:myprofile')

@login_required
def accept_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profiles.objects.get(pk=pk)
        receiver = Profiles.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'sent':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:myrequests')

@login_required
def decline_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profiles.objects.get(pk=pk)
        receiver = Profiles.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:myrequests')