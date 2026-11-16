package com.bastion.cuentas.application.exception;

import java.util.UUID;

public class CuentaNoEncontradaException extends RuntimeException {

    private final UUID cuentaId;

    public CuentaNoEncontradaException(UUID cuentaId) {
        super("No se encontró la cuenta con id: " + cuentaId);
        this.cuentaId = cuentaId;
    }

    public UUID cuentaId() {
        return cuentaId;
    }
}