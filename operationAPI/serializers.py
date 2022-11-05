from rest_framework import serializers

class OperationSerializer(serializers.Serializer):
    operation_type = serializers.CharField()
    x = serializers.IntegerField(required=False)
    y = serializers.IntegerField(required=False)
