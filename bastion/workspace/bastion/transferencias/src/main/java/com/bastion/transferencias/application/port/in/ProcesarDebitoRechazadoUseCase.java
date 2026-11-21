package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarDebitoRechazadoUseCase {

    void ejecutar(UUID transferenciaId, String motivo);
}