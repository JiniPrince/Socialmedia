from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api.models import Posts



class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","image"]
        widgets={
            "title":forms.Textarea(attrs={"class":"form-control border border-start-0 border-top-0 border-end-0","rows":3}),
            "image":forms.FileInput(attrs={"class":"form-select"})

        }
#for user registration
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]

#for user login                                                    
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()


#for add post
