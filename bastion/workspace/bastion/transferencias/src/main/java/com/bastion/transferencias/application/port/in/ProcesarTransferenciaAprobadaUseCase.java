package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarTransferenciaAprobadaUseCase {

    void ejecutar(UUID transferenciaId, UUID correlationId);
}