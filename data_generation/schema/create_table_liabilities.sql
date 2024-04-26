CREATE TABLE Liabilities (
    liability_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id UUID NOT NULL,
    liability_amount DECIMAL(18, 2) NOT NULL,
    interest_rate DECIMAL(5, 4),  -- NULL if not applicable
    start_date DATE,
    maturity_date DATE,
    counterparty_uuid UUID NOT NULL,
    status ENUM('Active', 'Paid Off', 'Defaulted') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID
);