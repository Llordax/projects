package com.bastion.cuentas.infrastructure.adapter.in.web.dto;

import java.util.UUID;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;

public record CrearCuentaRequest(

        @NotNull
        UUID titularId,

        @NotBlank
        @Pattern(regexp = "[A-Z]{3}", message = "La moneda debe ser un código ISO de tres letras, por ejemplo EUR")
        String moneda
) {
}