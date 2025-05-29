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
        device.assigment_status = True
        device.save()
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
        locations = Location.objects.select_related('user','device').distinct('device')

        device_type = request.query_params.get('device_type', None)
        user_id = request.query_params.get('user_id', None)
        if device_type:
            users = locations.filter(device__device_type=device_type)
        if user_id:
            users = locations.filter(id=user_id)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def devices(request):
    try:
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def unassign(request, id):
    try:
        device = Device.objects.get(pk=id)
        user = User.objects.get(device=device)
        device.assignment_status = False
        device.save()
        user.device = None
        user.save()
        return Response({
            "message": "Device unassigned successfully",
            "device_id": device.id,
            "user_id": user.id
        }, status=status.HTTP_200_OK)

    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


