from django.shortcuts import render
from api.models import Posts,Comments
from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
#to add user
class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

#to add post
class PostsView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=Posts.objects.all()
    #user must send login credentials to add post
    authentication_class=[authentication.BasicAuthentication]
    permission_class=[permissions.IsAuthenticated]

    #to save the login user
    #modelviewse-->perform_create()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    #list all the post of login user
    #login user have no id to list so detail=false
    #localhost:8000/posts/my_post/
    @action(methods=["GET"],detail=False)
    def my_post(self,request,*args,**kw):
        #get all post of login user
        qs=request.user.posts_set.all()
        se=PostSerializer(qs,many=True)
        return Response(data=se.data)

    #addcomment
    #localhost:8000/posts/1/add_comment/
    #modelviewset-pk for id
    #detail=True becoze pass id
    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kw):
        id=kw.get("pk")
        #get post of id=pk
        pos=Posts.objects.get(id=id)
        #corresponding user
        usr=request.user
        #data=comment,post=post,user=user
        se=CommentSerializer(data=request.data,context={"post":pos,"user":usr})
        if se.is_valid():
            #save comment only,to save user and post,override create method in commentserializer then here to save()
            se.save()
            return Response(data=se.data)
        else:
            return Response(data=se.errors)
    
    #LOCALHOST:8000/posts/1/list/comments/
    @action(methods=["get"],detail=True)
    def list_comments(self,request,*args,**kw):
        id=kw.get("pk")
        pos=Posts.objects.get(id=id)
        qs=pos.comments_set.all()
        se=CommentSerializer(qs,many=True)
        return Response(data=se.data)

class CommentsView(ModelViewSet):
    serializer_class=CommentSerializer
    queryset=Comments.objects.all()

    #authentication for user wanted to comment post of id=1,..
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    # localhost:8000/comments/1/like_comment
    @action(methods=["get"],detail=True)#detail=True because pass id of comment
    def like_comment(self,request,*args,**kw):
        com=self.get_object() #comment object,get_object() used to get the comment of id=1,..
        usr=request.user# user to like the above commment/login user to comment
        com.like.add(usr)
        return Response(data="created")