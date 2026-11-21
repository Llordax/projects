package com.bastion.transferencias.application.port.in;

import java.util.UUID;

public interface ProcesarCompensacionRealizadaUseCase {

	void ejecutar(UUID transferenciaId, UUID correlationId);
}