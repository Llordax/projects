package com.bastion.antifraude.domain.rule;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.Optional;

import com.bastion.antifraude.domain.model.SolicitudAntifraude;

public final class ImporteMaximoAntifraudeRegla implements ReglaAntifraude {

    private final BigDecimal importeMaximo;

    public ImporteMaximoAntifraudeRegla(BigDecimal importeMaximo) {
        this.importeMaximo = Objects.requireNonNull(
                importeMaximo,
                "importeMaximo no puede ser null"
        );

        if (importeMaximo.signum() <= 0) 
            throw new IllegalArgumentException("importeMaximo debe ser mayor que cero");
    }

    @Override
    public String codigo() {
        return "IMPORTE_MAXIMO";
    }

    @Override
    public Optional<String> evaluar(SolicitudAntifraude solicitud) {
        Objects.requireNonNull(solicitud, "solicitud no puede ser null");

        if (solicitud.importe().compareTo(importeMaximo) > 0) 
            return Optional.of("El importe supera el máximo permitido");

        return Optional.empty();
    }
}