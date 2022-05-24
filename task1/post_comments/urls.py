from unicodedata import name
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path("post/<int:id>",views.post,name='post'), 
    path('signup/', views.signup, name="handleSignUp"),
    path('login/', views.login_page, name="handleLogIn"),
    path('logout/', views.handleLogOut, name="handleLogOut"),
    path('postcomment/', views.postComment, name="postComment"),
    path('like/',views.like_post,name="like-post"),
    path('comment_delete/<int:id>',views.comment_delete,name="commentDelete"),
]