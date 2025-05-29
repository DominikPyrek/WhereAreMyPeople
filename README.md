# WhereAreMyPeople

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.1-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16.0-red.svg)](https://django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://postgresql.org)

A location tracking and people finding application that helps you stay connected with your friends and family.

## 🚀 Features

- **Device Management** - Create and manage tracking devices with serial numbers
- **User Registration** - Register users and assign devices to them
- **Device Assignment** - Assign/unassign devices to users with conflict checking
- **Location Tracking** - Record and retrieve real-time location pings from devices
- **Location History** - Store and access historical location data
- **Map View** - Get latest locations of all devices for map visualization
- **Device Filtering** - Filter devices by type and user
- **RESTful API** - Complete REST API for all operations

## 🛠️ Tech Stack

- **Backend:** Django 5.2.1 with Django REST Framework 3.16.0
- **Database:** PostgreSQL (via psycopg 3.2.9)
- **API:** RESTful API with filtering capabilities (django-filter 25.1)

## 🚦 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- [Python](https://python.org/) (version 3.8 or higher)
- [PostgreSQL](https://postgresql.org/) (version 12 or higher)
- [Git](https://git-scm.com/)
- [pip](https://pip.pypa.io/) (Python package manager)

### Installation
(before installation you need a postgres db setup can use the compose.yaml for docker)

1. Clone the repository
```bash
git clone https://github.com/DominikPyrek/WhereAreMyPeople.git
cd WhereAreMyPeople
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure Django settings
```bash
# Edit your Django settings.py file:
# - Change SECRET_KEY for security
# - Set DEBUG = False for production
# - Update DATABASES configuration for PostgreSQL
```

5. Set up the database
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server
```bash
python manage.py runserver
```

7. Open your browser and navigate to `http://localhost:8000`

### Configuration

Go to your Django settings file and update the following:

1. **Change the SECRET_KEY** for security
2. **Set DEBUG = False** for production use
3. **Update database settings** in the DATABASES configuration:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_database_name",
        "USER": "your_username", 
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

## 📖 Usage

### Basic Usage

1. **Create users** using the user creation endpoint
2. **Register devices** with serial numbers and device types
3. **Assign devices** to users (one device per user)
4. **Send location pings** from devices to track positions
5. **Retrieve locations** for individual users or view all devices on a map
6. **Unassign devices** when needed

## 🔧 API Documentation

The API is built with Django REST Framework and includes the following endpoints:

#### User Management
```python
POST /user/create
# Create a new user
# Body: {"first_name": "John", "last_name": "Doe"}
```

#### Device Management  
```python
POST /device/create
# Create a new device
# Body: {"serial_number": "ABC123", "device_type": "GPS_TRACKER"}

GET /devices/
# Get all devices

POST /devices/{id}/assign/
# Assign device to user
# Body: {"user_id": 1}

POST /devices/{id}/unassign/ 
# Unassign device from user
```

#### Location Tracking
```python
POST /devices/{id}/location/
# Send location ping from device
# Body: {"latitude": 52.2297, "longitude": 21.0122, "ping_time": "2024-01-01T12:00:00Z"}

GET /users/{id}/location/
# Get user's latest location

GET /map/
# Get latest locations of all devices
# Query params: ?device_type=GPS_TRACKER&user_id=1
```

## 📊 Data Models

### Device
- `id` - Primary key
- `serial_number` - Unique device identifier
- `device_type` - Type of device
- `assignment_status` - Whether device is assigned to user

### User  
- `id` - Primary key
- `first_name` - User's first name
- `last_name` - User's last name
- `device` - OneToOne relationship with Device

### Location
- `id` - Primary key
- `device` - Foreign key to Device
- `user` - Foreign key to User
- `ping_time` - Timestamp of location ping
- `latitude` - GPS latitude coordinate
- `longitude` - GPS longitude coordinate


## A short note:
If i had more time: 
a) Change how settings are handled by using .env files.
b) Make creating users and devices more robust.
c) Depending on the use case make GET's paginated.
d) Add API Throttling.
e) Added some type of auth (currently, anyone can modify data without restrictions).
f) Add code comments for clarity.
g) Search for a way to make querries better.
---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/DominikPyrek">Dominik Pyrek</a></p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
