from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


# Create your models here.
class Posts(models.Model):
    title=models.CharField(max_length=500)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    #likes=models.ManyToManyField(User,related_name="likes")

    #if list a post then  display the comment also for that,with highest count like
    #commentobject
    @property#used get_comment method as property of posts class and add in serializer fields
    def get_comment(self):
        qs=self.comments_set.all().annotate(u_count=Count('like')).order_by('-u_count')
        return qs


    def __str__(self):
        return self.title

class Comments(models.Model):
    Comment=models.CharField(max_length=5000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    like=models.ManyToManyField(User,related_name="like")
    #created_date=models.DateField(auto_now_add=True)
   
    def __str__(self):
        return self.Comment
    @property
    def like_count(self):
        return self.like.all().count()