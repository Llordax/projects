package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarCompensacionRechazadaUseCase {

    void ejecutar(UUID transferenciaId, String motivo);
}