package com.bastion.cuentas.application.port.in;

import java.math.BigDecimal;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;

public interface DebitarCuentaUseCase {

    Cuenta ejecutar(UUID cuentaId, UUID transferenciaId, BigDecimal importe);
}