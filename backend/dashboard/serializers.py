from rest_framework import serializers
from rest_framework import serializers
from .models import EnergyRecord, Chart

from .models import (
    EnergyRecord,
    Chart
)


class ChartSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Chart

        fields = "__all__"


class EnergyRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnergyRecord

        fields = [
            'id',
            'chart',
            'month',
            'consumption',
            'cost',
            'peak_load',
            'efficiency'
        ]

class ChartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Chart

        fields = "__all__"

        read_only_fields = ["user"]