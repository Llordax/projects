package com.bastion.eventos.contrato.cuentas;

import java.util.Objects;
import java.util.UUID;

public record CompensacionRechazadaData(UUID transferenciaId, UUID cuentaId, String motivo) {
	
	public CompensacionRechazadaData {
		Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");

        motivo = Objects.requireNonNull(motivo, "motivo no puede ser null").trim();
        if (motivo.isBlank()) 
            throw new IllegalArgumentException("motivo no puede estar vacío");
	}
}
