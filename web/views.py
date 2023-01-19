from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView,ListView
from .forms import LoginForm,UserRegistrationForm,PostForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Posts,Comments
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
        return wrapper

#for user registration
class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")


#for use login
class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})


#for homepage
@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    #after adding post rediect to the same page
    success_url=reverse_lazy("index")
   #list the posts
    model=Posts
    #post -saved object
    context_object_name="posts"
#validation of form bfore saving form -override form_valid
    def form_valid(self, form) :
        form.instance.user=self.request.user       
        messages.success(self.request,"your post added successfully")
        return super().form_valid(form)
    #exclude login user posts
    def get_queryset(self):
        return Posts.objects.exclude(user=self.request.user).order_by("-created_date")
#add comments  corresponding id post
#fn based view is used for button clicking

def post_delete_view(request,*args,**kw):
    id=kw.get("id")
    qs=Posts.objects.get(id=id).delete()
    messages.success(request,"Post has been deleted")
    return redirect("index")  
def add_comments(request,*args,**kw):
    id=kw.get("id")
    pos=Posts.objects.get(id=id)
    com=request.POST.get("comment")
    Comments.objects.create( post=pos,Comment=com,user=request.user) 
    messages.success(request,"your comment is posted" )
    return redirect("index")

def comment_delete_view(request,*args,**kw):
    id=kw.get("id")
    qs=Comments.objects.get(id=id).delete()
    messages.success(request,"comment has been deleted")
    return redirect("index") 

#add like to the comment of id -post
def comments_like(request,*args,**kw):
    id=kw.get("id")
    com=Comments.objects.get(id=id)
    com.like.add(request.user)
    return redirect("index")

def signout_view(request,*args,**kw):
    logout(request)  
    return redirect("signin")

    


