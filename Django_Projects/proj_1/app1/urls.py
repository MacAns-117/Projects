# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add/", views.details, name="add_patient"),
    path("patient/<str:Name>/", views.display, name="view_patient"),
    path('all/', views.view_all_patients, name='view_all_patients'),
    path('filter/', views.filter_patients, name='filter_patients'),
    path('patient/update/<int:id>/', views.update_patient, name='update_patient'),
    path('patient/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('base/',views.base, name="base"),
    path('base_login_signup/',views.base_login_signup ,name='base_login_signup'),
    path('', views.handlelogin, name='login'),
    path('signup/',views.signup,name='signup'),
    # Add other paths as needed
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
