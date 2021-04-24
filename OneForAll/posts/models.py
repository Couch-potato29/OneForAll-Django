from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.query_utils import FilteredRelation
from profiles.models import Profiles


class Post(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to = 'posts', validators = [FileExtensionValidator(['png','jpg','jpeg'])], blank = True)
    liked = models.ManyToManyField(Profiles, blank = True, related_name='likes')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.caption[:20])
    
    def likes_num(self):
        return self.liked.all().count()

    def comments_num(self):
        return self.comment_set.all().count()
        

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #return str(self.pk)
        return f"{self.pk}-{self.post.pk}-{self.user}"


LIKEORNO = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKEORNO, max_length=8)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"