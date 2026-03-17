from django.urls import path
from .views import CartListView, CartAddView, CartRemoveView

urlpatterns = [
    # List all cart items for the logged-in user
    path("cart/", CartListView.as_view(), name="cart-list"),

    # Add item to cart
    path("cart/add/", CartAddView.as_view(), name="cart-add"),

    # Remove item from cart by cart_id (UUID)
    path("cart/remove/<str:cart_id>/", CartRemoveView.as_view(), name="cart-remove"),
]
