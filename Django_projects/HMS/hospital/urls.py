from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [
    path('base_login_signup/',views.base_login_signup ,name='base_login_signup'),
    path('',views.login,name='login'),
    path('signup/',views.signup,name='signup')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)