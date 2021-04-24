from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profiles, Relationship

@receiver(post_save, sender = User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # print(sender)
    # print(instance)
    if created:
        Profiles.objects.create(user = instance)

@receiver(post_save, sender = Relationship)
def post_save_add_friend(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.followers.add(receiver_.user)
        receiver_.followers.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(pre_delete, sender = Relationship)
def deleting(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.followers.remove(receiver.user)
    receiver.followers.remove(sender.user)
    sender.save()
    receiver.save()