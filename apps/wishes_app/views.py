from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Wish, Like
from ..login_app.models import User
import datetime

#----------------------  Render routes -------------------#
#---------------------------------------------------------#

# Create your views here.
def index(request):
    user = User.objects.get(id = request.session["login_user"]["id"])
    granted_wishes = Wish.objects.filter(granted=True).order_by("-granted_date")
    print(granted_wishes.values())
    granted_wishes_with_likes = []
    for wish in granted_wishes:
        # get the number of likes
        likes = len(wish.likes.all()) 
        # check if current user like this granted wish
        if wish.user == user:
            hasLiked = True
        else:
            hasLiked = wish.likes.filter(user = user).exists()
        granted_wishes_with_likes.append({
            "granted_wish": wish,
            "likes": likes,
            "hasLiked": hasLiked,
        })
    context = {
        "wishes": Wish.objects.filter(granted=False, user = user).order_by("-created_at"),
        "granted_wishes": granted_wishes_with_likes,
    }
    return render(request, "wishes_app/wishes.html", context)

def new(request):
    return render(request, "wishes_app/add_wish.html")

def edit(request, wishId):
    context = {
        "wish": Wish.objects.get(id = wishId),
    }
    return render(request, "wishes_app/edit_wish.html", context)

def stats(request):
    user = User.objects.get(id = request.session["login_user"]["id"])
    total_granted_wishes = len(Wish.objects.filter(granted=True))
    user_granted_wishes = len(Wish.objects.filter(granted=True, user = user))
    user_pending_wishes = len(Wish.objects.filter(granted=False, user = user))
    context = {
        "total_granted_wishes": total_granted_wishes,
        "user_granted_wishes": user_granted_wishes,
        "user_pending_wishes": user_pending_wishes,
    }
    return render(request, "wishes_app/stats.html", context)

#------------------------- Redirect routes ----------------------#
#----------------------------------------------------------------#

def create(request):
    user = User.objects.get(id = request.session["login_user"]["id"])
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new") 
    # add wish in the database
    new_wish = Wish.objects.create(item = request.POST["item"],
                        desc = request.POST["desc"],
                        user = user)
    print(new_wish.__dict__)
    return redirect("/wishes")

def delete(request, wishId):
    Wish.objects.get(id = wishId).delete()
    return redirect("/wishes")

def update(request, wishId):
    # validation
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/wishes/edit/{wishId}") 
    wish = Wish.objects.get(id = wishId) 
    wish.item = request.POST['item']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect("/wishes")

def granted(request, wishId):
    wish = Wish.objects.get(id = wishId)
    wish.granted = True
    now_date = datetime.datetime.now()
    wish.granted_date = now_date
    wish.save()
    return redirect("/wishes")

def like(request, wishId):
    wish = Wish.objects.get(id = wishId)
    user = User.objects.get(id = request.session["login_user"]["id"])
    Like.objects.create(wish = wish, user = user)
    return redirect('/wishes')