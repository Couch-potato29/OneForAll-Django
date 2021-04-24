from .models import Profiles, Relationship
from posts.models import Post


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profiles.objects.get(user=request.user)
        pic = profile_obj.profile_pic
        return {'picture':pic}
    return {}

def requests_received(request):
    if request.user.is_authenticated:
        profile_obj = Profiles.objects.get(user=request.user)
        qs_count = Relationship.objects.requests_received(profile_obj).count()
        return {'request_no':qs_count}
    return {}

def user_posts(request):
    if request.user.is_authenticated:
        profile_obj = Profiles.objects.get(user=request.user)
        posts = Post.objects.all().filter(author=profile_obj)
        p_count = Post.objects.all().filter(author=profile_obj).count()
        return {'posts':posts,
        'count':p_count}
    return {}
