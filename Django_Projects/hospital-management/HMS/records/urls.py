from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/add/", views.patient_create, name="patient_create"),
    path("patients/<int:pk>/edit/", views.patient_update, name="patient_update"),
    path("patients/<int:pk>/delete/", views.patient_delete, name="patient_delete"),
    path("nurses/", views.nurse_list, name="nurse_list"),
    path("nurses/add/", views.nurse_create, name="nurse_create"),
    path("nurses/<int:pk>/edit/", views.nurse_update, name="nurse_update"),
    path("nurses/<int:pk>/delete/", views.nurse_delete, name="nurse_delete"),
]
