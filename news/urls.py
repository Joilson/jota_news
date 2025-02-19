from rest_framework.routers import DefaultRouter

from news.views.news import NewsViewSet

router = DefaultRouter()

router.register(r'news', NewsViewSet, basename='news')

urlpatterns = router.urls
