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
    path('profile/', ApplicationsByUserListView.as_view(), name='profile'),
    path('Application/new/', views.Application_new, name='Application_new'),
    path('delete/', views.ApplicationDelete.as_view(), name='delete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
