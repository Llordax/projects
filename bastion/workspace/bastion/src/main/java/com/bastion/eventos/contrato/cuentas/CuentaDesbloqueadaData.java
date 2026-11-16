package com.bastion.eventos.contrato.cuentas;

import java.util.Objects;
import java.util.UUID;

public record CuentaDesbloqueadaData(UUID cuentaId, String motivo) {
	
	public CuentaDesbloqueadaData {
		Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");

        motivo = Objects.requireNonNull(motivo, "motivo no puede ser null").trim();
        if (motivo.isBlank()) 
            throw new IllegalArgumentException("motivo no puede estar vacío");
	}
}
