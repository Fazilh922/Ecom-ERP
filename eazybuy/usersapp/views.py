from rest_framework import status, views,  generics
from rest_framework.response import Response
from .serializers import UserSerializer

class UserCreateView(views.APIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

