from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('contact/', views.contact_view, name='contact'),
]
