from typing import List, Dict

from rest_framework import serializers

from users.models import User
from users.models.plan import Plan
from users.serializers.plan import PlanSerializer
from users.serializers.validators.user import requires_plan_for_user_type_reader


class UserSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )
    plan_details = PlanSerializer(source="plan", read_only=True)

    type_details = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = list(field.name for field in User._meta.fields if field.name != 'is_superuser') + [
            'plan_details', 'type_details'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'plan_details': {'write_only': True}
        }

    def validate(self, attrs):
        requires_plan_for_user_type_reader(attrs)

        return attrs

    def get_type_details(self, obj) -> List[Dict[str, int | str]]:
        return [{"id": g.id, "name": g.name} for g in obj.groups.all()]
