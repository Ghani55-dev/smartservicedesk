from django.urls import path
from . import views
from .views import recent_activities
urlpatterns = [
    path('create/', views.create_ticket, name='create_ticket'),
    path('list/', views.ticket_list, name='ticket_list'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('api/recent-activities/', recent_activities, name='recent_activities')
]
