from django.urls import path

from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.index, name="main"),
    path("quotes/add_author", views.index, name="add_author"),
    path("quotes/add_quot", views.index, name="add_quot")
]
