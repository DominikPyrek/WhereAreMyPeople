from django.urls import path
from . import views

urlpatterns = [
    path('/devices/<int:id>/assign/', views.assign_device_to_user),
    path('/devices/<int:id>/location/', views.new_location_ping),
    path('/users/<int:id>/location/', views.get_user_location),
    path('/map/', views,latest_location_of_all_devices),
]