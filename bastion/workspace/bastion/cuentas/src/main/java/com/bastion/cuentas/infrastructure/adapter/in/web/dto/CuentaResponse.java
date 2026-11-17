package com.bastion.cuentas.infrastructure.adapter.in.web.dto;

import java.math.BigDecimal;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.EstadoCuenta;

public record CuentaResponse(
        UUID cuentaId,
        UUID titularId,
        String moneda,
        BigDecimal saldo,
        EstadoCuenta estado
) {

    public static CuentaResponse desdeDominio(Cuenta cuenta) {
        return new CuentaResponse(
                cuenta.id(),
                cuenta.titularId(),
                cuenta.moneda().getCurrencyCode(),
                cuenta.saldo(),
                cuenta.estado()
        );
    }
}