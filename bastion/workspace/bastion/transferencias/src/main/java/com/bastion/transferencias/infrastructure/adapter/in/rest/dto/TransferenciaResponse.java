package com.bastion.transferencias.infrastructure.adapter.in.rest.dto;

import java.math.BigDecimal;
import java.util.UUID;

import com.bastion.transferencias.domain.model.EstadoTransferencia;
import com.bastion.transferencias.domain.model.Transferencia;

public record TransferenciaResponse(
        UUID transferenciaId,
        UUID cuentaOrigenId,
        UUID cuentaDestinoId,
        BigDecimal importe,
        String moneda,
        EstadoTransferencia estado,
        String motivoRechazo
) {
    public static TransferenciaResponse desdeDominio(Transferencia transferencia) {
        return new TransferenciaResponse(
                transferencia.id(),
                transferencia.cuentaOrigenId(),
                transferencia.cuentaDestinoId(),
                transferencia.importe(),
                transferencia.moneda().getCurrencyCode(),
                transferencia.estado(),
                transferencia.motivoRechazo()
        );
    }
}