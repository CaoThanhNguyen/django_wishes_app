from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt, re

PASSWORD_REGEX = '\d.*[A-Z]|[A-Z].*\d'

# Create your views here.
def index(request):
    return render(request, "login_app/login.html")

def register(request):
    print(request.POST)
    # store current input data from the register form to re-display if needed
    request.session['input_data'] = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
    }
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    # check if that email is exist in the database
    user = User.objects.filter(email__iexact = request.POST['email']).first()
    # print(f"========= user={user}")
    if user:
        messages.error(request, "This email is already used. Please enter another one!")
        return redirect('/')
    # check if password has at least 1 number and 1 uppercase letter
    if not re.match(PASSWORD_REGEX, request.POST['password']):
        messages.error("Password should have at least 1 number and 1 uppercase letter")
        return redirect('/')
    # check if password is matched
    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request, "Passwords do not match. Please enter again!")
        return redirect('/')
    # hash password
    password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    # add new user in the database
    new_user = User.objects.create(first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    email = request.POST['email'],
                    password_hash = password_hash)
    # save new_user to the session
    request.session['login_user'] = {
        "id": new_user.id,
        "username": new_user.first_name,
    } 
    # messages.success(request, "You login successfully!")
    return redirect('/wishes')

# def success(request):
#     return render(request, "login_app/success.html")

def login(request):
    print(request.POST)
    # retrieve data from the database based on the email
    user = User.objects.filter(email__iexact=request.POST['email']).first()
    print(user)
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user.password_hash.encode()):
            print("password matched")
            # log this user in and store data in session
            request.session['login_user'] = {
                "id": user.id,
                "username": user.first_name,
            }
            return redirect('/wishes')
    messages.error(request, "You cannot log in. Please check your email and password again!")
    return redirect('/')

def logout(request):
    # clear session info
    try:
        del request.session['login_user']   
        del request.session['input_data']
    except KeyError:
        print("Warning! A KeyError exception occured when deleting session info") 
    return redirect('/')
    
