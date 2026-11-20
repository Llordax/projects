package com.bastion.antifraude.domain.model;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

public record SolicitudAntifraude(
        UUID transferenciaId,
        UUID cuentaOrigenId,
        UUID cuentaDestinoId,
        BigDecimal importe,
        Currency moneda
) {
    public SolicitudAntifraude {
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(cuentaOrigenId, "cuentaOrigenId no puede ser null");
        Objects.requireNonNull(cuentaDestinoId, "cuentaDestinoId no puede ser null");
        Objects.requireNonNull(importe, "importe no puede ser null");
        Objects.requireNonNull(moneda, "moneda no puede ser null");

        if (cuentaOrigenId.equals(cuentaDestinoId)) 
            throw new IllegalArgumentException(
                    "La cuenta de origen y la cuenta de destino deben ser distintas"
            );

        if (importe.signum() <= 0) 
            throw new IllegalArgumentException("importe debe ser mayor que cero");
    }
}