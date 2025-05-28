from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *

@api_view(['POST'])
def assign_device_to_user(request, id):
    try:
        device = Device.objects.get(pk=id)
        user = User.objects.get(pk=request.data.get('user_id'))
        if user.device:
            return Response({"error": "User has already been assigned to a device"}, status=status.HTTP_409_CONFLICT)
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
        if not device.device_user:
            return Response({"error": "No user has been asigned to the device"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def get_user_location(request, id):
    try:
        user = User.objects.get(pk=id)
        last_location = Location.objects.filter(user=user).last()
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def latest_location_of_all_devices(request):
    try:
        users = User.objects.filter(device__isnull=False).distinct()
        resoults = []
        for user in users:
            last_location = Location.objects.filter(user=user).last()
            results.append({
                    'user': user.id,
                    'device': user.device.id,
                    'location': LocationSerializer(last_loc).data
                })
        return Response(resoults)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

