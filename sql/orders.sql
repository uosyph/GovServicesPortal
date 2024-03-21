CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    details VARCHAR(4096),
    file_paths VARCHAR(4096),
    start_date DATETIME,
    end_date DATETIME,
    is_done BOOLEAN DEFAULT FALSE,
    service_id INT,
    user_id VARCHAR(14),
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
