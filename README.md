# Hotel Booking Manager

Hotel Booking Manager is a DBMS term project for managing hotel rooms, guests, bookings, and additional services.

The project consists of:

- PostgreSQL database
- FastAPI REST API
- Tkinter desktop frontend
- Docker Compose deployment for PostgreSQL and FastAPI
- Debian package (`.deb`) for the frontend

## Features

The application supports:

- Displaying hotel rooms
- Displaying bookings
- Creating new bookings
- Displaying booking statistics
- Creating additional services
- Preventing overlapping bookings for the same room
- API authentication using `X-API-Key`

## Technology Stack

- PostgreSQL
- Python
- FastAPI
- Psycopg
- Tkinter
- Docker
- Docker Compose
- Debian packaging

## Database Design

The database is normalized to Third Normal Form (3NF).

Tables:

- `guest`
- `room_category`
- `room`
- `booking`
- `service`
- `booking_service`

The `booking_service` table implements the N:M relationship between bookings and services.

Database files:

- `database/schema.sql`
- `database/seed.sql`

The database also contains an exclusion constraint that prevents overlapping active bookings for the same room.

## REST API

The FastAPI backend provides the following main endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/rooms` | List all rooms |
| GET | `/bookings` | List all bookings |
| GET | `/statistics/bookings` | Show booking statistics |
| POST | `/bookings` | Create a booking |
| POST | `/services` | Create a service |

The API documentation is available through Swagger UI at:

```text
http://localhost:8003/docs
```

## API Authentication

Write operations are protected with an `X-API-Key`.

Protected endpoints:

- `POST /bookings`
- `POST /services`

The API key is configured through the `.env` file and is not stored in the Git repository.

Example request header:

```text
X-API-Key: <your-api-key>
```

Requests without a valid API key return HTTP `401 Unauthorized`.

## Environment Configuration

Create a `.env` file in the project root.

Example:

```text
POSTGRES_DB=hotel_booking_ataleb
POSTGRES_USER=hotel_booking
POSTGRES_PASSWORD=<your-database-password>
API_KEY=<your-api-key>
```

The `.env` file is ignored by Git and must not be committed.

## Docker Compose Deployment

PostgreSQL and the FastAPI backend are started with Docker Compose.

From the project directory run:

```bash
docker compose up -d --build
```

Check the containers with:

```bash
docker compose ps
```

The PostgreSQL container initializes the database using:

- `database/schema.sql`
- `database/seed.sql`

The FastAPI backend is available on port `8003`.

To stop the containers:

```bash
docker compose down
```

## Frontend

The desktop frontend is implemented with Python and Tkinter.

At startup, the connection dialog asks for:

- API URL
- X-API-Key

For a local connection to the API:

```text
API URL: http://localhost:8003
```

The frontend communicates exclusively with the REST API and does not access PostgreSQL directly.

## Debian Package

The frontend is packaged as a Debian `.deb` package.

The generated package is:

```text
dist/hotel-booking-manager_1.0.0_all.deb
```

Build the package with:

```bash
mkdir -p dist
dpkg-deb --build packaging/hotel-booking-manager dist/hotel-booking-manager_1.0.0_all.deb
```

Inspect the package with:

```bash
dpkg-deb --info dist/hotel-booking-manager_1.0.0_all.deb
dpkg-deb --contents dist/hotel-booking-manager_1.0.0_all.deb
```

The package depends on:

- `python3`
- `python3-tk`

On a Debian system with administrator privileges, install it with:

```bash
sudo dpkg -i dist/hotel-booking-manager_1.0.0_all.deb
```

After installation, start the frontend with:

```bash
hotel-booking-manager
```

## Validation and Business Rules

### Booking validation

A booking requires:

```text
check_out > check_in
```

Invalid date ranges return HTTP `400 Bad Request`.

Overlapping active bookings for the same room are prevented by a PostgreSQL exclusion constraint.

An overlap returns HTTP `409 Conflict`.

### Service validation

Service prices must be non-negative.

Duplicate service names return HTTP `409 Conflict`.

## Project Structure

```text
DBMS_10/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── seed.sql
├── frontend/
│   └── main.py
├── packaging/
│   └── hotel-booking-manager/
├── dist/
│   └── hotel-booking-manager_1.0.0_all.deb
├── build/
├── compose.yaml
├── Makefile
├── README.md
└── .gitignore
```

## Tested Behavior

The implementation has been tested for:

- Docker Compose startup
- PostgreSQL health check
- Reading rooms through the API
- Creating bookings
- Creating services
- API-key authentication
- HTTP `401` for missing API key
- HTTP `409` for overlapping bookings
- Booking date validation
- Database foreign-key validation
- Debian package creation and inspection

## Project Scope

This project demonstrates:

- Relational database design
- Third Normal Form (3NF)
- Primary and foreign keys
- N:M relationships
- SQL constraints
- JOIN queries
- Aggregate queries
- REST API design
- API authentication
- Docker-based deployment
- Desktop frontend development
- Debian package creation
