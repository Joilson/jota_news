from django.conf import settings
from rest_framework import serializers

from news.models import News
from users.models.vertical import Vertical


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)  # API DOC como image no input
    image_url = serializers.SerializerMethodField(read_only=True)
    verticals = serializers.PrimaryKeyRelatedField(
        queryset=Vertical.objects.all(), many=True
    )

    class Meta:
        model = News
        fields = list(field.name for field in News._meta.fields) + ['image_url', 'verticals']
        extra_kwargs = {
            'author': {'required': False}
        }

    def get_image_url(self, obj):
        return f"{settings.FILE_STORAGE_URL}{obj.image.url}"

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            data["author"] = request.user
        return data
