from django.urls import path
from users.views import signup, signin,  signout

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', signin, name="login"),
    path('logout/', signout, name="logout")
]
