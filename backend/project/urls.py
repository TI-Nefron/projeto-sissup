from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('dialysis.urls')),
    path('api/', include('billing.urls')),
    path('api/', include('organization.urls')),
    path('api/', include('parameters.urls')),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

