
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('query/', query_builder, name='query'),

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/',manage_users, name='manage-users'),
    path('users/add/', add_user, name='add-user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete-user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
