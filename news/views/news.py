from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from news.models.news import News
from news.serializers.news import NewsSerializer
from news.services.news import NewsService
from news.views.permissions import IsEditorUser, IsReaderUser


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'patch']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser | IsEditorUser]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return News.objects.filter()

        return News.objects.filter(author=user)

    @action(detail=False, methods=["get"], permission_classes=[IsReaderUser])
    def for_readers(self, request):
        news = NewsService.find_for_readers(self.request.user)
        serializer = self.get_serializer(news, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        news = self.get_object()
        if news:
            serializer = self.get_serializer(news)
            return Response(serializer.data)
        return Response({"error": "News not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new = NewsService.create(serializer.validated_data)
            return Response(self.get_serializer(new).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        news = self.get_object()

        serializer = self.get_serializer(news, data=request.data, partial=False)
        if serializer.is_valid():
            updated_news = NewsService.update(news, serializer.validated_data)
            return Response(self.get_serializer(updated_news).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        news = self.get_object()
        serializer = self.get_serializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            updated_news = NewsService.update(news, serializer.validated_data)
            return Response(self.get_serializer(updated_news).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()

        NewsService.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
