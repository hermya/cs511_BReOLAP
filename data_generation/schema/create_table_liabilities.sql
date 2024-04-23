CREATE TABLE Liabilities (
    liability_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    liability_type_id INT NOT NULL,
    amount DECIMAL(18, 2) NOT NULL,
    interest_rate DECIMAL(5, 4),  -- NULL if not applicable
    start_date DATE,
    maturity_date DATE,
    counterparty_uuid UUID NOT NULL,
    currency_code CHAR(3) NOT NULL,
    status ENUM('Active', 'Paid Off', 'Defaulted') NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by UUID,  -- Assuming users are also managed in the system
    updated_by UUID,
	liability_types String
);