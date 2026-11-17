package com.bastion.transferencias.domain.model;

public enum EstadoTransferencia {

    SOLICITADA,
    PENDIENTE_ANTIFRAUDE,
    RECHAZADA,
    PENDIENTE_DEBITO,
    PENDIENTE_CREDITO,
    PENDIENTE_COMPENSACION,
    COMPLETADA,
    COMPENSADA,
    ERROR_COMPENSACION
}