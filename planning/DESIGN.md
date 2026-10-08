# Campus Parking System - Design Document

## Architecture Overview

### System Components
1. **User Service** - Authentication and user management
2. **Parking Service** - Parking lot and space management
3. **Reservation Service** - Booking and reservation handling
4. **Notification Service** - Real-time updates and alerts
5. **Admin Service** - Administrative operations

## Database Schema

### Users Table
```
- user_id (PK)
- username
- email
- password_hash
- role (admin, faculty, student)
- created_at
```

### Parking Lots Table
```
- lot_id (PK)
- name
- location
- total_spaces
- capacity
- created_at
```

### Parking Spaces Table
```
- space_id (PK)
- lot_id (FK)
- space_number
- category (regular, accessible, reserved)
- is_available
- last_updated
```

### Reservations Table
```
- reservation_id (PK)
- user_id (FK)
- space_id (FK)
- start_time
- end_time
- status
- created_at
```

## API Endpoints

### User Endpoints
- POST /api/users/register - Register new user
- POST /api/users/login - User login
- GET /api/users/profile - Get user profile
- PUT /api/users/profile - Update user profile

### Parking Endpoints
- GET /api/lots - List all parking lots
- GET /api/lots/{lot_id}/spaces - Get spaces in lot
- GET /api/spaces/available - Get available spaces

### Reservation Endpoints
- POST /api/reservations - Create reservation
- GET /api/reservations - Get user reservations
- DELETE /api/reservations/{id} - Cancel reservation

### Admin Endpoints
- POST /api/admin/lots - Create parking lot
- PUT /api/admin/lots/{id} - Update parking lot
- GET /api/admin/reports - Generate reports
