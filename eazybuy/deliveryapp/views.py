from rest_framework import views
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderTrackView(views.APIView):
    def get(self, request, tracking_number):
        order = Order.objects.get(tracking_number=tracking_number)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
