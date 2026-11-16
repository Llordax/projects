package com.bastion.eventos.contrato.cuentas;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Locale;
import java.util.Objects;
import java.util.UUID;

public record CompensacionSolicitadaData(
		UUID transferenciaId,
        UUID cuentaId,
        BigDecimal importe,
        String moneda,
        String motivo
) {
	
	public CompensacionSolicitadaData {
		Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        Objects.requireNonNull(importe, "importe no puede ser null");

        if (importe.signum() <= 0) 
            throw new IllegalArgumentException("importe debe ser mayor que cero");

        moneda = Objects.requireNonNull(moneda, "moneda no puede ser null")
                .trim()
                .toUpperCase(Locale.ROOT);

        try {
            Currency.getInstance(moneda);
        } catch (IllegalArgumentException exception) {
            throw new IllegalArgumentException("moneda debe ser un código ISO 4217 reconocido", exception);
        }

        motivo = Objects.requireNonNull(motivo, "motivo no puede ser null").trim();
        if (motivo.isBlank()) 
            throw new IllegalArgumentException("motivo no puede estar vacío");
	}
}
