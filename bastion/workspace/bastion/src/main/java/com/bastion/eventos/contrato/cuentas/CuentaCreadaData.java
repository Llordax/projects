package com.bastion.eventos.contrato.cuentas;

import java.util.Currency;
import java.util.Locale;
import java.util.Objects;
import java.util.UUID;

public record CuentaCreadaData(UUID cuentaId, UUID titularId, String moneda) {
	
	public CuentaCreadaData {
		Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        Objects.requireNonNull(titularId, "titularId no puede ser null");

        moneda = Objects.requireNonNull(moneda, "moneda no puede ser null")
                .trim()
                .toUpperCase(Locale.ROOT);

        try {
            Currency.getInstance(moneda);
        } catch (IllegalArgumentException exception) {
            throw new IllegalArgumentException("moneda debe ser un código ISO 4217 reconocido", exception);
        }
	}
}
