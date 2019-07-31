CREATE SCHEMA dev;
CREATE TABLE dev.vehicle (
    vehicle_id SERIAL PRIMARY KEY,
    key VARCHAR(36) NOT NULL,
    user_id INTEGER,
    is_booked BOOLEAN NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE dev.vehicle IS
'Stores Vehicle Information';