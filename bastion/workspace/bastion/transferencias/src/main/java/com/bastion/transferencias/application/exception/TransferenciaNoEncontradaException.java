package com.bastion.transferencias.application.exception;

import java.util.UUID;

public class TransferenciaNoEncontradaException extends RuntimeException {

    private final UUID transferenciaId;

    public TransferenciaNoEncontradaException(UUID transferenciaId) {
        super("No se encontró la transferencia con id: " + transferenciaId);
        this.transferenciaId = transferenciaId;
    }

    public UUID transferenciaId() {
        return transferenciaId;
    }
}