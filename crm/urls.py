from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashbord, name="dashboard"),
    path("leads/", views.leads, name="leads"),
    path("leads/<int:id>/", views.lead_detail, name="lead-detail"),
    path("leads/create/", views.create_lead, name="create"),
    path("leads/<int:id>/update/", views.update_lead, name="update"),
    path("lead/<int:id>/delete", views.delete_lead, name="delete"),
    
]