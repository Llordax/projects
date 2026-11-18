package com.bastion.cuentas.application.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.DebitarCuentaUseCase;
import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.ReglaCuentaException;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.DebitoRealizadoData;
import com.bastion.eventos.contrato.cuentas.DebitoRechazadoData;

@Service
public class DebitarCuentaService implements DebitarCuentaUseCase {

    private final CuentaRepository cuentaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public DebitarCuentaService(
            CuentaRepository cuentaRepository,
            EventoOutboxPort eventoOutboxPort
    ) {
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
    public Cuenta ejecutar(UUID cuentaId, UUID transferenciaId, BigDecimal importe) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");

        Cuenta cuenta = cuentaRepository.buscarPorId(cuentaId)
                .orElseThrow(() -> new CuentaNoEncontradaException(cuentaId));

        try {
            cuenta.debitar(importe);
        } catch (ReglaCuentaException excepcion) {
            registrarDebitoRechazado(cuenta, transferenciaId, excepcion);
            throw excepcion;
        }

        Cuenta cuentaGuardada = cuentaRepository.guardar(cuenta);
        UUID eventId = UUID.randomUUID();

        Evento<DebitoRealizadoData> evento = new Evento<>(
                eventId,
                TiposEvento.DEBITO_REALIZADO,
                1,
                Instant.now(),
                cuentaGuardada.id().toString(),
                transferenciaId,
                new DebitoRealizadoData(
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

    private void registrarDebitoRechazado(
            Cuenta cuenta,
            UUID transferenciaId,
            ReglaCuentaException excepcion
    ) {
        UUID eventId = UUID.randomUUID();
        String motivo = excepcion.getMessage() != null
                ? excepcion.getMessage()
                : excepcion.codigo().name();

        Evento<DebitoRechazadoData> evento = new Evento<>(
                eventId,
                TiposEvento.DEBITO_RECHAZADO,
                1,
                Instant.now(),
                cuenta.id().toString(),
                transferenciaId,
                new DebitoRechazadoData(
                        transferenciaId,
                        cuenta.id(),
                        motivo
                )
        );

        eventoOutboxPort.registrarRechazo(evento);
    }
}