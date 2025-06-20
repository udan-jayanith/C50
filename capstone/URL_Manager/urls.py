from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('libraries/<int:ownerPk>', views.libraries, name='libraries'),
    path('libraries/<int:ownerPk>/<int:pageNo>', views.getLibraries, name='getLibraries'),
    path('publicLibraries', views.publicLibraries, name='publicLibraries'),
    path('publicLibraries/<int:pageNo>', views.getPublicLibraries, name='getPublicLibraries'),
    path('myLibraries', views.myLibrariesPage, name='myLibraries'),
    path('library/<int:libraryPk>', views.library, name='library'),
    path('library/<int:libraryPk>/edit', views.editLibrary, name='editLibrary'),
    path('library/<int:libraryPk>/delete', views.deleteLibrary, name='deleteLibrary'),
    path('getUrls/<int:libraryPk>/<int:pageNo>', views.getUrls, name='getUrls'),
    path('', views.index, name='index'),
]
