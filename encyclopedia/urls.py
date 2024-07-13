from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.page, name="page"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),
    path("edit/<str:page>", views.edit, name="edit"),
]
