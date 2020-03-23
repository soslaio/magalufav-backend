
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from core import views

router = routers.DefaultRouter()
router.register('favorites', views.FavoritosViewSet, basename='favorites')
router.register('customers', views.ClientesViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
