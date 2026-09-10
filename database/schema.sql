CREATE TABLE guest (
    guest_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(30)
);
CREATE TABLE room_category (
    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    price_per_night NUMERIC(10,2) NOT NULL CHECK (price_per_night >= 0)
);
CREATE TABLE room (
    room_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    room_number VARCHAR(20) UNIQUE NOT NULL,
    floor INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES room_category(category_id)
);
CREATE TABLE booking (
    booking_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
    guest_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id),
    CHECK (check_out > check_in),
    CHECK (status IN ('confirmed', 'checked_in', 'checked_out', 'cancelled'))
);
CREATE TABLE service (
    service_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0)
);
CREATE TABLE booking_service (
    booking_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    PRIMARY KEY (booking_id, service_id),
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
    FOREIGN KEY (service_id) REFERENCES service(service_id)
);
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE booking
ADD CONSTRAINT no_overlapping_bookings
EXCLUDE USING gist (
    room_id WITH =,
    daterange(check_in, check_out, '[)') WITH &&
)
WHERE (status IN ('confirmed', 'checked_in'));
