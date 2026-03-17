from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static

from cart.views import CartViewSet, CartListView, CartView
from products.views import ProductViewSet  
from order.views import OrderViewSet

# ✅ Router for ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Router
    path('api/', include(router.urls)),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Accounts
    path('api/', include('accounts.urls')),

    # Cart endpoints for extra actions
    path('api/cart/', CartListView.as_view(), name='cart-list'),
    path('api/cart/<int:pk>/update-quantity/', CartViewSet.as_view({'patch': 'update_quantity'}), name='update-quantity'),
    path('api/cart/<int:pk>/', CartView.as_view(), name='cart-detail'),

    # Orders extra actions
    path('api/orders/<int:pk>/cancel/', OrderViewSet.as_view({'post': 'cancel'}), name='order-cancel'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
