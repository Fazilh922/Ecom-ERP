from django.urls import path
from . import views
from .views import reset_password
from .views import UserCreateView, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('login/', LoginView.as_view(), name='user-login'),  # Login API view (LoginView)
      path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # JWT Token Views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # HTML login page (non-API view)
    path('', views.login_view, name='login'),  # Update this to login_view for the HTML page
    
    path('register/', views.register, name='register'),  # Register page
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('index/', views.index, name='index'),
    path('reset-password/', reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

