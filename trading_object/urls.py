from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TradingObjectViewSet

# Создаем экземпляр DefaultRouter
router = DefaultRouter()
# Регистрируем TradingViewSet с именем 'trading-object'
router.register(r"trading_object", TradingObjectViewSet, basename="trading-object")

urlpatterns = [
    path("", include(router.urls)),
]
