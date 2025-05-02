from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'securities', views.SecurityViewSet)
router.register(r'investments', views.InvestmentViewSet)
router.register(r'deposits', views.DepositViewSet)
router.register(r'securities/(?P<security_pk>\d+)/quotes', views.QuoteHistoryViewSet, basename='quotes')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('', include(router.urls)),
    
]