from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers.user import UserSerializer
from users.services.user import UserService


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def list(self, request):
        news = UserService.list()
        serializer = UserSerializer(news, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        news = UserService.get(pk)
        if news:
            serializer = UserSerializer(news)
            return Response(serializer.data)
        return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new = UserService.create(serializer.validated_data)
            return Response(UserSerializer(new).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = UserService.get(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=False)  # full update
        if serializer.is_valid():
            updated_user = UserService.update(user, serializer.validated_data)
            return Response(UserSerializer(updated_user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        deleted_count = UserService.delete(pk)
        if deleted_count:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
