from django.db import models
from django.shortcuts import reverse
from django.db.models import aggregates
from django.db.models.deletion import CASCADE
from django.db.models.fields import SlugField
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from .utils import get_randomcode
from django.db.models import Q
from django.template.defaultfilters import slugify
# Create your models here.
CATEGORY_CHOICES = (
    ('Startup Member','Startup Member'),
    ('Investor','Investor')
)

FIELDS = (
    ('Technology','Technology'),
    ('Textiles','Textiles'),
    ('Sculptures and Paintings','Sculptures and Paintings'),
    ('Sports','Sports'),
    ('Music','Music'),
    ('Food and Health','Food and Health')
)

class ProfileManager(models.Manager):

    def get_profiles_to_request(self, sender):
        profiles = Profiles.objects.all().exclude(user = sender)
        profile = Profiles.objects.get(user = sender)
        qs = Relationship.objects.filter(Q(sender=profile)| Q(receiver=profile))
        print(qs)

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        profile = Profiles.objects.all().exclude(user=me)
        return profile

class Profiles(models.Model):
    first_name = models.CharField(max_length=200, blank = True)
    last_name = models.CharField(max_length=200, blank = True)
    user = models.OneToOneField(User, on_delete=CASCADE)
    about = models.TextField(default = "no bio", max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Startup Member')
    field_of_interest = models.CharField(max_length = 50, choices=FIELDS, default='NONE')
    email = models.EmailField(max_length=200,blank = True)
    country = models.CharField(max_length=200,blank = True)
    profile_pic = models.ImageField(default = 'avatar.png',upload_to = 'profile_pic/')
    followers = models.ManyToManyField(User, blank = True,related_name = 'followers')
    slug = models.SlugField(unique=True,blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    def get_absolute_url(self):
        return reverse("profiles:profile_details", kwargs = {"slug":self.slug})
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def get_followers(self):
        return self.followers.all()
    
    def get_follow_count(self):
        return self.followers.all().count()

    def get_no_of_posts(self):
        return self.posts.all().count()
    
    def get_posts(self):
        return self.posts.all()
    
    def likes_given(self):
        likes = self.like_set.all()
        total_likes = 0
        for i in likes:
            if i.value == 'Like':
                total_likes+=1
        return total_likes

    def likes_received(self):
        posts = self.posts.all()
        total_likes = 0
        for post in posts:
            total_likes += post.liked.all().count()
        return total_likes
    
    def save(self, *args,**kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name)+" "+str(self.last_name))
                ex = Profiles.objects.filter(slug = to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_randomcode))
                    ex = Profiles.objects.filter(slug = to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)

STATUS_CHOICES = (
    ('sent','sent'),
    ('accepted','accepted')
)

class RelationshipManager(models.Manager):
    def requests_received(self, receiver):
        queryset = Relationship.objects.filter(receiver=receiver, status = 'sent')
        return queryset



class Relationship(models.Model):
    sender = models.ForeignKey(Profiles, on_delete = CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profiles, on_delete = CASCADE, related_name='receiver')
    status = models.CharField(max_length=10, choices = STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"