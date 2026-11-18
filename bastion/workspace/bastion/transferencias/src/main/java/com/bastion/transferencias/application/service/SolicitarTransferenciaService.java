package com.bastion.transferencias.application.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.transferencias.TransferenciaSolicitadaData;
import com.bastion.transferencias.application.port.in.SolicitarTransferenciaUseCase;
import com.bastion.transferencias.application.port.out.EventoOutboxPort;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.Transferencia;

@Service
public class SolicitarTransferenciaService implements SolicitarTransferenciaUseCase {

    private final TransferenciaRepository transferenciaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public SolicitarTransferenciaService(
            TransferenciaRepository transferenciaRepository,
            EventoOutboxPort eventoOutboxPort
    ) {
        this.transferenciaRepository = Objects.requireNonNull(
                transferenciaRepository,
                "transferenciaRepository no puede ser null"
        );
        this.eventoOutboxPort = Objects.requireNonNull(
                eventoOutboxPort,
                "eventoOutboxPort no puede ser null"
        );
    }

    @Override
    @Transactional
    public Transferencia ejecutar(
            UUID cuentaOrigenId,
            UUID cuentaDestinoId,
            BigDecimal importe,
            Currency moneda
    ) {
        Transferencia transferencia = new Transferencia(
                UUID.randomUUID(),
                cuentaOrigenId,
                cuentaDestinoId,
                importe,
                moneda
        );

        transferencia.iniciarEvaluacionAntifraude();
        Transferencia guardada = transferenciaRepository.guardar(transferencia);

        UUID eventId = UUID.randomUUID();
        Evento<TransferenciaSolicitadaData> evento = new Evento<>(
                eventId,
                TiposEvento.TRANSFERENCIA_SOLICITADA,
                1,
                Instant.now(),
                guardada.id().toString(),
                guardada.id(),
                new TransferenciaSolicitadaData(
                        guardada.id(),
                        guardada.cuentaOrigenId(),
                        guardada.cuentaDestinoId(),
                        guardada.importe(),
                        guardada.moneda().getCurrencyCode()
                )
        );

        eventoOutboxPort.registrar(evento);
        return guardada;
    }
}