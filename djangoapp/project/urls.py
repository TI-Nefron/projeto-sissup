from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from dialysis import views as dialysis_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dialysis.urls')),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'dialysis/',
        include('dialysis.urls', namespace='dialysis')
    ),

    path(
        '',
        dialysis_views.dashboard_view,
        name='dashboard'
    ),
]