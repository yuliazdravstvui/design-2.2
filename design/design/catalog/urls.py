from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', ApplicationListView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', views.registration, name='registration'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('validate_username', validate_username, name='validate_username'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),


    path('admin_base/', views.ApplicationListViewAdmin.as_view(), name='admin_base'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('creating_category/', views.CategoryCreate.as_view(), name='creating_category'),
    path('change/<int:pk>/status/', views.ChangeStatusRequest.as_view(), name='change_status'),

    path('application/', ApplicationViewUser.as_view(), name='my_application'),
    path('create/', ApplicationCreate.as_view(), name='create'),
    path('request/<pk>/delete/', ApplicationDelete.as_view(), name='delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
