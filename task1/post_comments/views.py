from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import BlogComment, Like, Post

# Create your views here.


def index(request):
    myposts = Post.objects.all()
    user = request.user
    context = {"myposts": myposts, "user": user}
    return render(request, "index.html", context)


def post(request, id):
    post = Post.objects.filter(post_id=id)[0]
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():

            replyDict[reply.parent.sno] = [reply]

        else:
            replyDict[reply.parent.sno].append(reply)

    context = {"post": post, "comments": comments, "user": request.user, "replyDict": replyDict}
    return render(request, "post.html", context)


def like_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(post_id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        like.save()
    return redirect("/")


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(post_id=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/post/{post.post_id}")


def comment_delete(request, id):
    comment = BlogComment.objects.filter(sno=id)
    comment.delete()
    messages.success(request, "Your comment has been successfully deleted")
    return redirect("/")


def login_page(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpass"]

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return render(request, "login.html")


def handleLogOut(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")


def signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstName"]
        lname = request.POST["lastName"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect("home")
        if pass1 != pass2:
            messages.error(request, " Passwords do not match")
            return redirect("home")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect("home")
    else:
        return render(request, "signup.html")
