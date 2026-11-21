package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarCreditoRealizadoUseCase {

    void ejecutar(UUID transferenciaId, UUID correlationId);
}