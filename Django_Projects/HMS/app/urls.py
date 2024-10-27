from django.urls import path
from .views import login_view, register_view, dashboard, nurses, add_nurse, update_nurse, logout_view, delete_nurse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('nurses/', nurses, name='nurses'),
    path('add_nurse/', add_nurse, name='add_nurse'),
    path('update_nurse/<int:nurse_id>/', update_nurse, name='update_nurse'),
    path('delete_nurse/<int:nurse_id>/', delete_nurse, name='delete_nurse'),  # Add this line

    path('logout/', logout_view, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# from django.urls import path
# from .views import login_view, register_view, dashboard, nurses, add_nurse, update_nurse, logout_view
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('', login_view, name='login'),
#     path('register/', register_view, name='register'),
#     path('dashboard/', dashboard, name='dashboard'),
#     path('nurses/', nurses, name='nurses'),
#     path('add_nurse/', add_nurse, name='add_nurse'),
#     path('update_nurse/<int:nurse_id>/', update_nurse, name='update_nurse'),
#     path('logout/', logout_view, name='logout'),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
