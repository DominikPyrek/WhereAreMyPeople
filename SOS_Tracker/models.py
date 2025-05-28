from django.db import models
from django.db.models import SET_NULL

class Device(models.Model):

    serial_number = models.CharField(max_length=40)

    def __str__(self):
        last_location = self.device_locations.last()
        user = getattr(self, 'device_user', None)

        if user and last_location:
            return (f"Device number:{self.id} serial:{self.serial_number} "
            f"last seen:{last_location.timestamp} at "
            f"latitude:{last_location.latitude}, "
            f"longitude:{last_location.longitude}, "
            f"owner:{user.first_name}, {user.last_name}"
            )

        return f"Device number:{self.id} serial: {self.serial_number}"

class User(models.Model):

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    device = models.OneToOneField(
        Device,
        null=True, 
        blank=True, 
        unique=True, 
        related_name="device_user", 
        on_delete=models.SET_NULL)

    def __str__(self):
        last_location = self.device.device_locations.last() if self.device else None

        if last_location:
            return (f"User:{self.first_name} {self.last_name} "
            f"last seen:{last_location.timestamp} at "
            f"latitude:{last_location.latitude} "
            f"longitude:{last_location.longitude}"
            )

        return f"User:{self.first_name} {self.last_name}"


class Location(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="device_locations")
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):

        if self.user:
            return(f"Location:{self.id} at "
            f"latitude:{self.latitude} "
            f"longitude:{self.longitude} "
            f"time:{self.timestamp} "
            f"user:{self.user.first_name} {self.user.last_name}"
            )

        return(f"Location:{self.id} at "
            f"latitude:{self.latitude} "
            f"longitude:{self.longitude} "
            f"time:{self.timestamp} "
            )