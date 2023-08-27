from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from .views import RegisterView

app_name = "users"

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("signin/",
         LoginView.as_view(template_name="users/signin.html", form_class=LoginForm, redirect_authenticated_user=True),
         name="signin"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]