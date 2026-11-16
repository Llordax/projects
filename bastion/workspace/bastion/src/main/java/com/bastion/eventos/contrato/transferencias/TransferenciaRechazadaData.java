package com.bastion.eventos.contrato.transferencias;

import java.util.Objects;
import java.util.UUID;

public record TransferenciaRechazadaData(UUID transferenciaId,String motivo) {
	
	public TransferenciaRechazadaData {
		Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");

        motivo = Objects.requireNonNull(motivo, "motivo no puede ser null").trim();
        if (motivo.isBlank()) 
            throw new IllegalArgumentException("motivo no puede estar vacío");
	}
}
