package com.bastion.transferencias.application.service;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.DebitoSolicitadoData;
import com.bastion.transferencias.application.exception.TransferenciaNoEncontradaException;
import com.bastion.transferencias.application.port.in.ProcesarTransferenciaAprobadaUseCase;
import com.bastion.transferencias.application.port.out.EventoOutboxPort;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.Transferencia;

@Service
public class ProcesarTransferenciaAprobadaService
        implements ProcesarTransferenciaAprobadaUseCase {

    private final TransferenciaRepository transferenciaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public ProcesarTransferenciaAprobadaService(
            TransferenciaRepository transferenciaRepository,
            EventoOutboxPort eventoOutboxPort) {
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
    public void ejecutar(UUID transferenciaId, UUID correlationId) {
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(correlationId, "correlationId no puede ser null");

        Transferencia transferencia = transferenciaRepository.buscarPorId(transferenciaId)
                .orElseThrow(() ->
                        new TransferenciaNoEncontradaException(transferenciaId));

        transferencia.aprobarAntifraude();
        Transferencia guardada = transferenciaRepository.guardar(transferencia);

        UUID eventId = UUID.randomUUID();
        Evento<DebitoSolicitadoData> evento = new Evento<>(
                eventId,
                TiposEvento.DEBITO_SOLICITADO,
                1,
                Instant.now(),
                guardada.id().toString(),
                correlationId,
                new DebitoSolicitadoData(
                        guardada.id(),
                        guardada.cuentaOrigenId(),
                        guardada.importe(),
                        guardada.moneda().getCurrencyCode()
                )
        );

        eventoOutboxPort.registrar(evento);
    }
}