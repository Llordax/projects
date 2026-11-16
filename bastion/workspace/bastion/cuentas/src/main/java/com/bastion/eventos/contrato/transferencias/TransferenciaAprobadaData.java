package com.bastion.eventos.contrato.transferencias;

import java.util.List;
import java.util.Objects;
import java.util.UUID;

public record TransferenciaAprobadaData(UUID transferenciaId,List<String> reglasAplicadas) {
	
	public TransferenciaAprobadaData {
		Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(reglasAplicadas, "reglasAplicadas no puede ser null");

        reglasAplicadas = List.copyOf(reglasAplicadas);

        for (String regla : reglasAplicadas) 
            if (regla.isBlank()) 
                throw new IllegalArgumentException("Las reglas aplicadas no pueden contener valores vacíos");
	}
}
