CREATE TABLE transferencias (
    id UUID PRIMARY KEY,
    cuenta_origen_id UUID NOT NULL,
    cuenta_destino_id UUID NOT NULL,
    importe NUMERIC(19, 4) NOT NULL,
    moneda VARCHAR(3) NOT NULL,
    estado VARCHAR(40) NOT NULL,
    motivo_rechazo VARCHAR(500),
    version BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT chk_transferencias_importe_positivo
        CHECK (importe > 0),

    CONSTRAINT chk_transferencias_cuentas_distintas
        CHECK (cuenta_origen_id <> cuenta_destino_id)
);

CREATE INDEX idx_transferencias_cuenta_origen
    ON transferencias (cuenta_origen_id);

CREATE INDEX idx_transferencias_cuenta_destino
    ON transferencias (cuenta_destino_id);