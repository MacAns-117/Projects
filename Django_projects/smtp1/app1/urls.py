from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.handlelogin,name='login'),
    path('signup/', views.signup, name='signup'),
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('newrequest/',views.newrequest,name='newrequest'),
    path('approved/<int:req_id>/', views.approved, name='approved'),
    path('rejected/<int:req_id>/',views.rejected,name='rejected'),
    path('request_form/',views.request_form,name='request_form'),
    path('base/',views.base,name='base'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
