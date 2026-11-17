package com.bastion.cuentas.application.service;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.BloquearCuentaUseCase;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CuentaBloqueadaData;

@Service
public class BloquearCuentaService implements BloquearCuentaUseCase {

    private final CuentaRepository cuentaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public BloquearCuentaService(
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
    public boolean ejecutar(UUID cuentaId, String motivo) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        String motivoNormalizado = Objects.requireNonNull(
                motivo,
                "motivo no puede ser null"
        ).trim();

        if (motivoNormalizado.isBlank()) {
            throw new IllegalArgumentException("motivo no puede estar vacío");
        }

        Cuenta cuenta = cuentaRepository.buscarPorId(cuentaId)
                .orElseThrow(() -> new CuentaNoEncontradaException(cuentaId));

        boolean cambioRealizado = cuenta.bloquear();

        if (!cambioRealizado) {
            return false;
        }

        Cuenta cuentaGuardada = cuentaRepository.guardar(cuenta);
        UUID eventId = UUID.randomUUID();

        Evento<CuentaBloqueadaData> evento = new Evento<>(
                eventId,
                TiposEvento.CUENTA_BLOQUEADA,
                1,
                Instant.now(),
                cuentaGuardada.id().toString(),
                eventId,
                new CuentaBloqueadaData(cuentaGuardada.id(), motivoNormalizado)
        );

        eventoOutboxPort.registrar(evento);
        return true;
    }
}