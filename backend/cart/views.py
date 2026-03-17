from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cart.cassandra_models import add_to_cart, get_cart_items  # Your Cassandra helper functions
import uuid

class CartListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Use Cassandra helper to get cart items
        cart_items = get_cart_items(user_id=str(request.user.id))
        return Response({"cart": list(cart_items)}, status=status.HTTP_200_OK)

class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST)

        cart_id = add_to_cart(user_id=str(request.user.id), product_id=str(product_id), quantity=quantity)
        return Response({"message": "Item added to cart", "cart_id": str(cart_id)}, status=status.HTTP_201_CREATED)

class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, cart_id=None):
        # Delete item by cart_id in Cassandra
        from cart.cassandra_models import session
        query = "DELETE FROM cart WHERE cart_id=%s"
        session.execute(query, (uuid.UUID(cart_id),))
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
