package com.bastion.cuentas.application.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.AcreditarCuentaUseCase;
import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CreditoRealizadoData;

@Service
public class AcreditarCuentaService implements AcreditarCuentaUseCase {

    private final CuentaRepository cuentaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public AcreditarCuentaService(
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

        cuenta.acreditar(importe);
        Cuenta cuentaGuardada = cuentaRepository.guardar(cuenta);

        UUID eventId = UUID.randomUUID();
        Evento<CreditoRealizadoData> evento = new Evento<>(
                eventId,
                TiposEvento.CREDITO_REALIZADO,
                1,
                Instant.now(),
                cuentaGuardada.id().toString(),
                transferenciaId,
                new CreditoRealizadoData(
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
}