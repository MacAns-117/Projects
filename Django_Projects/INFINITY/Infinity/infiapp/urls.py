
from django.urls import path
from infiapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.home,name="home"),
    path("index",views.index, name="index"),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
