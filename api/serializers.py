from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Posts,Comments

#to add user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","username","password"]
    #password hashed- create_user()
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    post=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    like_count=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=["id","Comment","post","user","like_count"]   

    def create(self, validated_data):
        #validated_data=comment
        pos=self.context.get("post")
        usr=self.context.get("user")
        return pos.comments_set.create(user=usr,**validated_data)
     

#to add post
class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
   # likes=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    get_comment=CommentSerializer(read_only=True,many=True)
    
    class Meta:
        model=Posts
        fields=["id",
            "title",
            "image",
            "user",
            "created_date","get_comment"

        ]


    