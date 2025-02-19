from rest_framework import serializers
from users.models.user import UserType


def requires_plan_for_user_type_reader(data):
    user_type = data.get("type")
    plan = data.get("plan")

    if user_type == UserType.READER.value and not plan:
        raise serializers.ValidationError({"plan": "Is required when user type is reader."})

    return data
