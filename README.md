# Hotel Booking Manager

Hotel Booking Manager is a database-backed desktop application for managing room reservations in a small hotel.

The project was developed as a term project for the course **Introduction to Database Management Systems** at THGA Bochum.

## Features

The application provides the following functionality:

- Display hotel rooms and room categories
- Display existing bookings with guest and room information
- Create new bookings
- Prevent overlapping bookings for the same room
- Display booking statistics
- Create additional hotel services
- Protect write operations with an X-API-Key
- Desktop user interface for interacting with the REST API

## Technology Stack

- **Database:** PostgreSQL
- **Backend:** Python, FastAPI
- **Database Driver:** psycopg
- **Frontend:** Python, Tkinter
- **API Documentation:** Swagger / OpenAPI

## Database

The relational database contains the following tables:

- `guest`
- `room_category`
- `room`
- `booking`
- `service`
- `booking_service`

The schema is designed in **Third Normal Form (3NF)**.

Primary keys and foreign keys are used to maintain referential integrity.

An exclusion constraint prevents overlapping bookings for the same room and time period.

Database files are located in:

```text
database/schema.sql
database/seed.sql
```

## REST API

The FastAPI backend provides the following project endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/rooms` | Returns rooms together with room category information |
| GET | `/bookings` | Returns bookings together with guest and room information |
| GET | `/statistics/bookings` | Returns aggregated booking statistics |
| POST | `/bookings` | Creates a new booking |
| POST | `/services` | Creates a new hotel service |

The API also provides the root endpoint `/` as a simple health check.

## API Authentication

Write operations require the HTTP header:

```text
X-API-Key: hotel-booking-key
```

The protected endpoints are:

```text
POST /bookings
POST /services
```

Requests without the correct API key return HTTP status `401 Unauthorized`.

## Booking Validation

When a booking is created, the backend validates the request.

Examples:

- Check-out must be after check-in.
- Guest and room must exist.
- A room cannot have overlapping bookings.

An overlapping booking returns:

```text
409 Conflict
Room is already booked for this period
```

## Service Validation

When a service is created:

- The price must not be negative.
- The service name must be unique.

Duplicate service names return HTTP status `409 Conflict`.

## Running the Backend

Create and activate a Python virtual environment and install the required Python packages.

The backend can then be started with:

```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8003
```

The API documentation is available at:

```text
http://localhost:8003/docs
```

## Running the Frontend

The frontend is located in:

```text
frontend/main.py
```

Start it with:

```bash
python frontend/main.py
```

The desktop application connects to:

```text
http://localhost:8003
```

If the backend runs on a remote server, an SSH tunnel can be used to forward port `8003` to the local computer.

## Frontend Views

The desktop application contains the following views:

- Connection
- Main Menu
- Rooms
- Bookings
- Create Booking
- Booking Statistics
- Add Service

The Rooms view also displays the database Room ID so that the correct room can be selected when creating a booking.

## Project Structure

```text
DBMS_10/
├── backend/
│   └── main.py
├── database/
│   ├── schema.sql
│   └── seed.sql
├── frontend/
│   └── main.py
├── proposal-template/
├── src/
├── README.md
└── Makefile
```

## Tested Behaviour

The implementation was tested for:

- Database connectivity
- Reading rooms
- Reading bookings
- Booking statistics
- Creating valid bookings
- Rejecting overlapping bookings
- Rejecting invalid booking dates
- Creating hotel services
- Rejecting duplicate service names
- Rejecting write requests without an X-API-Key
- Accepting write requests with the correct X-API-Key
- Frontend communication with the FastAPI backend

## Project Scope

The implementation follows the REST API scope defined in the project proposal. The five main project endpoints are implemented together with the PostgreSQL database and Tkinter desktop frontend.
