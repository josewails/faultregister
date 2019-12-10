from rest_framework import serializers
from core.models import Chart


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = "__all__"
