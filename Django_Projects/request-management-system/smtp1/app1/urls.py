from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("request/", views.request_form, name="request_form"),
    path("adminpanel/", views.adminpanel, name="adminpanel"),
    path("approved/<int:req_id>/", views.approved, name="approved"),
    path("rejected/<int:req_id>/", views.rejected, name="rejected"),
]
