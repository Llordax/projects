package com.bastion.transferencias.infrastructure.adapter.in.rest.dto;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record SolicitarTransferenciaRequest(
        @NotNull UUID cuentaOrigenId,
        @NotNull UUID cuentaDestinoId,
        @NotNull
        @DecimalMin(value = "0.0", inclusive = false)
        BigDecimal importe,
        @NotBlank
        @Pattern(regexp = "^[A-Z]{3}$", message = "La moneda debe ser un código ISO de tres letras")
        String moneda
) {
}