CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128),
    description VARCHAR(432),
    readme TEXT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
