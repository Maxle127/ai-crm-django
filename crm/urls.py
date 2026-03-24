from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashbord, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("leads/", views.leads, name="leads"),
    path("leads/<int:id>/", views.lead_detail, name="lead-detail"),
    path("leads/create/", views.LeadCreateView.as_view(), name="create"),
    path("leads/<int:pk>/update/", views.LeadUpdateView.as_view(), name="update"),
    path("lead/<int:pk>/delete/", views.LeadDeleteView.as_view(), name="delete"),

]