from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashbord, name="dashboard"),
    path("leads/", views.leads, name="leads"),
    path("leads/<int:id>", views.lead_detail, name="lead-detail")
]