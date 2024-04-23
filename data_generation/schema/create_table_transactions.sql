CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_uuid UUID DEFAULT (uuid_generate_v4()),
    transaction_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type ENUM('Payment', 'Withdrawal', 'InterestPayment', 'LoanRepayment', 'Other') NOT NULL,
    due_date DATE NOT NULL,
    description VARCHAR(255),
    category ENUM('Operational', 'Financial', 'ClientWithdrawal', 'Contingent', 'Regulatory') NOT NULL,
    confirmed BOOLEAN DEFAULT FALSE,
    asset_linked UUID,
    counterparty_uuid UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);