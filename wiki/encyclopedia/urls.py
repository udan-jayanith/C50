from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="wiki-homepage"),
    path('wiki/<str:title>/', views.wikiContent, name='wiki-content'),
    path('search/', views.search, name='search-wiki'),
    path('createNewPage/', views.createNewPage, name='createNewPage'),
    path('wiki/<str:title>/edit', views.editWiki, name='edit-wiki'),
    path('wiki/random-page', views.randomWiki, name='random-wiki'),
]
