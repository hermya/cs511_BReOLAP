CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_uuid UUID DEFAULT (uuid_generate_v4()),
    transaction_date DATE NOT NULL,
    transaction_amount DECIMAL(15, 2) NOT NULL,
    transaction_type ENUM('Payment', 'Withdrawal', 'InterestPayment', 'LoanRepayment', 'Other') NOT NULL,
    transaction_due_date DATE NOT NULL,
    transaction_category ENUM('Operational', 'Financial', 'ClientWithdrawal', 'Contingent', 'Regulatory') NOT NULL,
    transaction_confirmed BOOLEAN DEFAULT FALSE,
    asset_linked UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);