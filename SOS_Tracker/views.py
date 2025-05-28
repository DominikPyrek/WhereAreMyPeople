from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_device(request):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_device_to_user(request, id):
    try:
        device = Device.objects.get(pk=id)
        user = User.objects.get(pk=request.data.get('user_id'))

        if user.device:
            return Response({"error": "User has already been assigned to a device"}, status=status.HTTP_409_CONFLICT)
        if hasattr(device, 'device_user'):
            return Response({"error": "Device is already assigned to user"},status=status.HTTP_409_CONFLICT)

        user.device = device
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def new_location_ping(request, id):
    try:
        device = Device.objects.get(pk=id)
        if not hasattr(device, 'device_user'):
            return Response({"error": "No user has been asigned to the device"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'device': device.id,
            'user': device.device_user.id,
            'ping_time': request.data.get('ping_time'),
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude']
        }

        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_location(request, id):
    try:
        user = User.objects.get(pk=id)
        last_location = Location.objects.filter(user=user).last()
        if not last_location:
            return Response({"error": "No Pings yet"}, status=status.HTTP_404_NOT_FOUND)
        serialzer = LocationSerializer(last_location)
        return Response(serialzer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def latest_location_of_all_devices(request):
    try:
        users = User.objects.filter(device__isnull=False).distinct()
        results = []
        for user in users:
            last_location = Location.objects.filter(user=user).last()
            results.append({
                    'user': user.id,
                    'device': user.device.id,
                    'latitude': last_location.latitude,
                    'longitude': last_location.longitude,
                    'ping_time': last_location.ping_time
                })
        return Response(results)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

