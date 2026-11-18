package com.bastion.cuentas.infrastructure.adapter.in.rest.dto;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.NotNull;

public record MovimientoCuentaRequest(

        @NotNull(message = "El identificador de transferencia es obligatorio")
        UUID transferenciaId,

        @NotNull(message = "El importe es obligatorio")
        @DecimalMin(
                value = "0.0",
                inclusive = false,
                message = "El importe debe ser mayor que cero"
        )
        @Digits(
                integer = 15,
                fraction = 4,
                message = "El importe admite hasta 15 dígitos enteros y 4 decimales"
        )
        BigDecimal importe
) {
}