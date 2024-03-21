CREATE TABLE users (
    id VARCHAR(14) PRIMARY KEY,
    password VARCHAR(224),
    name VARCHAR(128),
    phone VARCHAR(16),
    email VARCHAR(48),
    address VARCHAR(128),
    is_admin BOOLEAN DEFAULT FALSE
);
