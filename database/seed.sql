INSERT INTO room_category (name, capacity, price_per_night)
VALUES
    ('Single', 1, 79.00),
    ('Double', 2, 119.00),
    ('Suite', 4, 199.00);
INSERT INTO room (room_number, floor, active, category_id)
VALUES
    ('101', 1, TRUE, 1),
    ('102', 1, TRUE, 1),
    ('201', 2, TRUE, 2),
    ('202', 2, TRUE, 2),
    ('301', 3, TRUE, 3);
INSERT INTO guest (first_name, last_name, email, phone)
VALUES
    ('Anna', 'Schmidt', 'anna.schmidt@example.com', '+49 170 1234567'),
    ('Max', 'Mueller', 'max.mueller@example.com', '+49 171 7654321'),
    ('Laura', 'Weber', 'laura.weber@example.com', '+49 172 9876543');
INSERT INTO service (name, price)
VALUES
    ('Breakfast', 15.00),
    ('Parking', 10.00),
    ('Late Check-out', 25.00);
INSERT INTO booking (check_in, check_out, status, guest_id, room_id)
VALUES
    ('2026-09-10', '2026-09-13', 'confirmed', 1, 1),
    ('2026-09-15', '2026-09-18', 'confirmed', 2, 3),
    ('2026-09-20', '2026-09-25', 'confirmed', 3, 5);
INSERT INTO booking_service (booking_id, service_id, quantity)
VALUES
    (1, 1, 2),
    (1, 2, 1),
    (2, 1, 2),
    (3, 3, 1);
