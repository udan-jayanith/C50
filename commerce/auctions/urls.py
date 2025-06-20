from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('addListing', views.addListing, name='addListing'),
    path('listing/<int:pk>', views.listingPage, name='listing'),
    path('category', views.categoryPage, name='categoryPage'),
    path('addComment', views.addComment, name='addComment'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('listing/<int:pk>/placeBid', views.placeBid, name='place-bid'),
    path('category/<str:category>', views.categoryFilter, name='categoryFilter'),
    path('listing/<int:pk>/end', views.endAuction, name = 'endAuction'),
    path('inbox', views.inbox, name='inbox')
]
