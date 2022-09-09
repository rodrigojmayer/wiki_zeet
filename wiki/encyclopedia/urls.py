from django.urls import path

from . import views

app_name="encyclopedias"

urlpatterns = [
    path("", views.index, name="index"),
    #path("wiki/CSS", views.CSS, name="CSS"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:entry_name>", views.edit, name="edit"),
    path("random_entry/", views.random_entry, name="random_entry")
]