from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search_result/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit/<str:title>/", views.edit, name="edit")
]
