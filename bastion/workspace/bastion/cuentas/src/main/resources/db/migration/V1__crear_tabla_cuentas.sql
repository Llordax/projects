CREATE TABLE cuentas (
    id UUID PRIMARY KEY,
    titular_id UUID NOT NULL,
    moneda VARCHAR(3) NOT NULL,
    saldo NUMERIC(19, 4) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    version BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT ck_cuentas_saldo_no_negativo
        CHECK (saldo >= 0),

    CONSTRAINT ck_cuentas_estado_valido
        CHECK (estado IN ('ACTIVA', 'BLOQUEADA'))
);

CREATE INDEX ix_cuentas_titular_id
    ON cuentas (titular_id);