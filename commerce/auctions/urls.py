from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category", views.category_index, name="category_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/category", views.category_watchlist, name="category_watchlist"),
    path("watchlist/remove/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
]
