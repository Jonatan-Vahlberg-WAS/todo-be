from django.urls import path
from . import views
urlpatterns = [
    path('', views.api_overview, name="api-overview"),
    path('lists/', views.get_lists, name="lists"),
    path('lists/list/<str:pk>/', views.get_list, name="list"),
    path('lists/update/<str:pk>/', views.update_list, name="list-update"),
    path('lists/create/', views.create_list, name="list-create"),
]