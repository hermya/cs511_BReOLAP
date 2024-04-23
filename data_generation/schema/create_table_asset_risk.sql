CREATE TABLE AssetRisks (
    asset_uuid UUID NOT NULL,
    risk_uuid UUID NOT NULL,
    risk_factor FLOAT NOT NULL,
    PRIMARY KEY (asset_uuid, risk_uuid)
);
