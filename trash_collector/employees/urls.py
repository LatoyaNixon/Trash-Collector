from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('date_of_last_pickup/<int:customer_id>', views.date_of_last_pickup_confirmation, name="date_of_last_pickup"),
    path('filter_by_day/', views.filter_customer_by_day, name="filter_by_day"),
]
    
    
    