CREATE TABLE Counterparties (
    counterparty_id INT AUTO_INCREMENT PRIMARY KEY,
    counterparty_uuid UUID,
    counterparty_name VARCHAR(255) NOT NULL,
    counterparty_type ENUM('Individual', 'Institution', 'Company', 'Other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);