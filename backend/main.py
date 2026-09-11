from fastapi import FastAPI, HTTPException, Header
import os
import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel
from datetime import date


app = FastAPI(title="Hotel Booking Manager API")

API_KEY = "hotel-booking-key"


class BookingCreate(BaseModel):
    check_in: date
    check_out: date
    guest_id: int
    room_id: int


class ServiceCreate(BaseModel):
    name: str
    price: float


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "hotel_booking_ataleb"),
        user=os.getenv("DB_USER", "ataleb"),
        password=os.getenv("DB_PASSWORD", ""),
        row_factory=dict_row
    )


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing X-API-Key"
        )


@app.get("/")
def root():
    return {
        "message": "Hotel Booking Manager API is running"
    }


@app.get("/rooms")
def get_rooms():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    r.room_id,
                    r.room_number,
                    r.floor,
                    r.active,
                    rc.name AS category,
                    rc.capacity,
                    rc.price_per_night
                FROM room r
                JOIN room_category rc
                    ON r.category_id = rc.category_id
                ORDER BY r.room_number;
            """)

            return cur.fetchall()


@app.get("/bookings")
def get_bookings():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    b.booking_id,
                    b.check_in,
                    b.check_out,
                    b.status,
                    g.guest_id,
                    g.first_name,
                    g.last_name,
                    r.room_id,
                    r.room_number
                FROM booking b
                JOIN guest g
                    ON b.guest_id = g.guest_id
                JOIN room r
                    ON b.room_id = r.room_id
                ORDER BY b.booking_id;
            """)

            return cur.fetchall()


@app.get("/statistics/bookings")
def get_booking_statistics():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_bookings,

                    COUNT(*) FILTER (
                        WHERE status = 'confirmed'
                    ) AS confirmed_bookings,

                    COUNT(*) FILTER (
                        WHERE status = 'checked_in'
                    ) AS checked_in_bookings,

                    COUNT(*) FILTER (
                        WHERE status = 'checked_out'
                    ) AS checked_out_bookings,

                    COUNT(*) FILTER (
                        WHERE status = 'cancelled'
                    ) AS cancelled_bookings

                FROM booking;
            """)

            return cur.fetchone()


@app.post("/bookings", status_code=201)
def create_booking(
    booking: BookingCreate,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    if booking.check_out <= booking.check_in:
        raise HTTPException(
            status_code=400,
            detail="check_out must be after check_in"
        )

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO booking (
                        check_in,
                        check_out,
                        status,
                        guest_id,
                        room_id
                    )
                    VALUES (
                        %s,
                        %s,
                        'confirmed',
                        %s,
                        %s
                    )
                    RETURNING
                        booking_id,
                        check_in,
                        check_out,
                        status,
                        guest_id,
                        room_id;
                """, (
                    booking.check_in,
                    booking.check_out,
                    booking.guest_id,
                    booking.room_id
                ))

                return cur.fetchone()

    except psycopg.errors.ExclusionViolation:
        raise HTTPException(
            status_code=409,
            detail="Room is already booked for this period"
        )

    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=400,
            detail="Guest or room does not exist"
        )


@app.post("/services", status_code=201)
def create_service(
    service: ServiceCreate,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    if service.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be non-negative"
        )

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO service (
                        name,
                        price
                    )
                    VALUES (
                        %s,
                        %s
                    )
                    RETURNING
                        service_id,
                        name,
                        price;
                """, (
                    service.name,
                    service.price
                ))

                return cur.fetchone()

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Service name already exists"
        )
