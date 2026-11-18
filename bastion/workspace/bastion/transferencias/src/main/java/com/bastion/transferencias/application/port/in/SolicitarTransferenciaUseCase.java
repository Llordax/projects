package com.bastion.transferencias.application.port.in;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import com.bastion.transferencias.domain.model.Transferencia;

public interface SolicitarTransferenciaUseCase {

    Transferencia ejecutar(
            UUID cuentaOrigenId,
            UUID cuentaDestinoId,
            BigDecimal importe,
            Currency moneda
    );
}