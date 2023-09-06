from django.urls import path

from . import views

app_name = "quotes_app"

urlpatterns = [
    path("", views.index, name="main"),
    path("quotes/add_author", views.add_author, name="add_author"),
    path("quotes/add_quot", views.add_quot, name="add_quot"),
    path("quotes/author_page", views.author_page, name="author_page"),
    path("quotes/tags_search", views.tags_search, name="tags_search")

]
