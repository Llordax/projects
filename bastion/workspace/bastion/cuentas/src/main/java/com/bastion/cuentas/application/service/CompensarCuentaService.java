package com.bastion.cuentas.application.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;
import java.util.UUID;
import java.util.Currency;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.CompensarCuentaUseCase;
import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.ReglaCuentaException;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CompensacionRealizadaData;
import com.bastion.eventos.contrato.cuentas.CompensacionRechazadaData;

@Service
public class CompensarCuentaService implements CompensarCuentaUseCase {

    private final CuentaRepository cuentaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public CompensarCuentaService(
            CuentaRepository cuentaRepository,
            EventoOutboxPort eventoOutboxPort) {
        this.cuentaRepository = Objects.requireNonNull(
                cuentaRepository,
                "cuentaRepository no puede ser null"
        );
        this.eventoOutboxPort = Objects.requireNonNull(
                eventoOutboxPort,
                "eventoOutboxPort no puede ser null"
        );
    }

    @Override
    @Transactional
    public Cuenta ejecutar(UUID cuentaId, UUID transferenciaId, BigDecimal importe, Currency moneda) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(importe, "importe no puede ser null");

        Cuenta cuenta;

        try {
            cuenta = cuentaRepository.buscarPorId(cuentaId)
                    .orElseThrow(() -> new CuentaNoEncontradaException(cuentaId));
        } catch (CuentaNoEncontradaException excepcion) {
            registrarCompensacionRechazada(cuentaId, transferenciaId, excepcion.getMessage());
            throw excepcion;
        }

        try {
            if (moneda != null) {
                cuenta.validarMoneda(moneda);
            }
            cuenta.acreditar(importe);
        } catch (ReglaCuentaException excepcion) {
            registrarCompensacionRechazada(cuentaId, transferenciaId, excepcion.getMessage());
            throw excepcion;
        }
        Cuenta cuentaGuardada = cuentaRepository.guardar(cuenta);

        UUID eventId = UUID.randomUUID();
        Evento<CompensacionRealizadaData> evento = new Evento<>(
                eventId,
                TiposEvento.COMPENSACION_REALIZADA,
                1,
                Instant.now(),
                cuentaGuardada.id().toString(),
                transferenciaId,
                new CompensacionRealizadaData(
                        transferenciaId,
                        cuentaGuardada.id(),
                        importe,
                        cuentaGuardada.saldo(),
                        cuentaGuardada.moneda().getCurrencyCode()
                )
        );

        eventoOutboxPort.registrar(evento);
        return cuentaGuardada;
    }

    private void registrarCompensacionRechazada(
            UUID cuentaId,
            UUID transferenciaId,
            String motivo
    ) {
        UUID eventId = UUID.randomUUID();
        Evento<CompensacionRechazadaData> evento = new Evento<>(
                eventId,
                TiposEvento.COMPENSACION_RECHAZADA,
                1,
                Instant.now(),
                cuentaId.toString(),
                transferenciaId,
                new CompensacionRechazadaData(
                        transferenciaId,
                        cuentaId,
                        motivo
                )
        );

        eventoOutboxPort.registrarRechazo(evento);
    }
}
