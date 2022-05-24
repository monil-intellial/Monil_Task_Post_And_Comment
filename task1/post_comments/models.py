from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30,default="")
    author = models.CharField(max_length=30,default="")
    content = models.TextField(max_length=200,default="")
    liked = models.ManyToManyField(User,default=None, blank=True)
    pub_date = models.DateField()

    def __str__(self):
        return self.title
    
    @property
    def num_likes(self):
        return self.liked.all().count()
    

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True)    
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username
    

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like',max_length=10)

    def __str__(self):
        return str(self.post)