package com.bastion.cuentas.application.service;

import java.time.Instant;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.port.in.CrearCuentaUseCase;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CuentaCreadaData;

@Service
public class CrearCuentaService implements CrearCuentaUseCase {

    private final CuentaRepository cuentaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public CrearCuentaService(
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
    public Cuenta ejecutar(UUID titularId, Currency moneda) {
        Cuenta cuenta = new Cuenta(UUID.randomUUID(), titularId, moneda);
        Cuenta cuentaGuardada = cuentaRepository.guardar(cuenta);

        UUID eventId = UUID.randomUUID();
        Evento<CuentaCreadaData> evento = new Evento<>(
                eventId,
                TiposEvento.CUENTA_CREADA,
                1,
                Instant.now(),
                cuentaGuardada.id().toString(),
                eventId,
                new CuentaCreadaData(
                        cuentaGuardada.id(),
                        cuentaGuardada.titularId(),
                        cuentaGuardada.moneda().getCurrencyCode()
                )
        );

        eventoOutboxPort.registrar(evento);

        return cuentaGuardada;
    }
}