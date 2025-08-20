from django.urls import path
from users.views import signup, signin,  signout, demo

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('logout/', signout, name="logout"),
    path('demo/', demo, name="demo")
]
