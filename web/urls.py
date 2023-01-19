from django.urls import path
from .views import SignInView,SignUpView,IndexView,add_comments,comments_like,signout_view,post_delete_view,comment_delete_view
urlpatterns = [
      path("",SignInView.as_view(),name="signin"),
      path("register",SignUpView.as_view(),name="signup"),
      path("index",IndexView.as_view(),name="index"),
      path("posts/<int:id>/comments/add",add_comments,name="add_comments"),
      path("posts/<int:id>/remove",post_delete_view,name="post-delete"),
      path("comments/<int:id>/like/add",comments_like,name="comments_like"),
      path("comments/<int:id>/remove",comment_delete_view,name="comment-delete"),
      path("logout",signout_view,name="sign_out"),
]