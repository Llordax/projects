package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarCreditoRechazadoUseCase {

    void ejecutar(UUID transferenciaId, String motivo, UUID correlationId);
}