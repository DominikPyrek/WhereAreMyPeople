from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'device')

class LocationSerializer(serializers.ModelSerializer):
    device_serial = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ('id', 'user', 'device_serial', 'latitude', 'longitude', 'timestamp')

    def get_device_serial(self, obj):
        if obj.user and obj.user.device:
            return obj.user.device.serial_number
        return None