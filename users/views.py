from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomRegistrationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def signup(request):
    if request.method == "GET":
        form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
 
    context = {
        "form": form,
    }

    return render(request, "signup.html", context)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"usernaem = {username}\npassword = {password}")
        user = authenticate(request, username=username, password=password)
        print(f"log in as a {user}")
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('signin')

def demo(request):
    if request.method == "GET":
        form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST) 

        if form.is_valid():
            form.save()
 
    context = {
        "form": form,
    }

    return render(request, "base.html", context)

